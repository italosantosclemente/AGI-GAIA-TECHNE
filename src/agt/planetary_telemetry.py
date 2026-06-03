from __future__ import annotations

import csv
import io
import json
import math
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any, Callable, Dict, Iterable, List, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


FetchText = Callable[[str], str]

USGS_DAY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
NASA_EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100"
NOAA_CO2_DAILY_URL = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_daily_mlo.csv"
WORLD_BANK_URL = "https://api.worldbank.org/v2/country/WLD/indicator/{indicator}?format=json&per_page=8"
GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=timelinevol&format=json&timespan=1d"


@dataclass(frozen=True)
class TelemetrySignal:
    domain: str
    name: str
    value: str
    unit: str = ""
    observed_at: str = ""
    source: str = ""
    url: str = ""
    status: str = "ok"
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlanetaryTelemetryReport:
    generated_at: str
    generated_unix: float
    command: str
    signals: List[TelemetrySignal]
    tension_index: int
    judgment: str
    summary: str
    failures: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "generated_unix": self.generated_unix,
            "command": self.command,
            "tension_index": self.tension_index,
            "judgment": self.judgment,
            "summary": self.summary,
            "signals": [signal.to_dict() for signal in self.signals],
            "failures": self.failures,
        }


class PlanetaryTelemetry:
    """
    Finite, sourced planetary telemetry.

    This is not Gaia's omniscience. It is a public symbolic instrument that
    samples a few open sources each time the operator asks for telemetry.
    """

    def __init__(
        self,
        fetch_text: Optional[FetchText] = None,
        timeout: int = 20,
    ) -> None:
        self.fetch_text = fetch_text or (lambda url: fetch_url_text(url, timeout=timeout))

    def collect(self) -> PlanetaryTelemetryReport:
        generated = datetime.now(timezone.utc)
        signals: List[TelemetrySignal] = []
        failures: List[str] = []

        for collector in (
            self._collect_noaa_co2,
            self._collect_usgs_earthquakes,
            self._collect_nasa_eonet,
            self._collect_world_bank,
            self._collect_gdelt,
        ):
            try:
                signals.extend(collector())
            except Exception as exc:
                failures.append(f"{collector.__name__}: {exc}")

        tension_index = compute_tension_index(signals)
        judgment = classify_tension(tension_index)
        summary = build_summary(signals, failures, tension_index, judgment)
        return PlanetaryTelemetryReport(
            generated_at=generated.isoformat(),
            generated_unix=generated.timestamp(),
            command="fazer telemetria",
            signals=signals,
            tension_index=tension_index,
            judgment=judgment,
            summary=summary,
            failures=failures,
        )

    def _collect_noaa_co2(self) -> List[TelemetrySignal]:
        text = self.fetch_text(NOAA_CO2_DAILY_URL)
        latest = latest_noaa_daily_co2(text)
        if latest is None:
            return [failed_signal("environment", "Atmospheric CO2", NOAA_CO2_DAILY_URL, "no valid row")]
        date, ppm = latest
        return [
            TelemetrySignal(
                domain="environment",
                name="Atmospheric CO2 at Mauna Loa",
                value=f"{ppm:.2f}",
                unit="ppm",
                observed_at=date,
                source="NOAA GML Mauna Loa daily CO2",
                url=NOAA_CO2_DAILY_URL,
                note="NOAA notes recent values may be revised after quality control.",
            )
        ]

    def _collect_usgs_earthquakes(self) -> List[TelemetrySignal]:
        payload = json.loads(self.fetch_text(USGS_DAY_URL))
        features = payload.get("features", [])
        magnitudes = [
            float(feature.get("properties", {}).get("mag"))
            for feature in features
            if feature.get("properties", {}).get("mag") is not None
        ]
        max_mag = max(magnitudes) if magnitudes else 0.0
        m45_count = sum(1 for mag in magnitudes if mag >= 4.5)
        generated = payload.get("metadata", {}).get("generated")
        observed_at = (
            datetime.fromtimestamp(generated / 1000, tz=timezone.utc).isoformat()
            if isinstance(generated, (int, float))
            else ""
        )
        return [
            TelemetrySignal(
                domain="geophysical",
                name="Earthquakes in past day",
                value=str(len(features)),
                unit="events",
                observed_at=observed_at,
                source="USGS all earthquakes, past day",
                url=USGS_DAY_URL,
            ),
            TelemetrySignal(
                domain="geophysical",
                name="Largest earthquake magnitude in past day",
                value=f"{max_mag:.1f}",
                unit="Mw",
                observed_at=observed_at,
                source="USGS all earthquakes, past day",
                url=USGS_DAY_URL,
            ),
            TelemetrySignal(
                domain="geophysical",
                name="M4.5+ earthquakes in past day",
                value=str(m45_count),
                unit="events",
                observed_at=observed_at,
                source="USGS all earthquakes, past day",
                url=USGS_DAY_URL,
            ),
        ]

    def _collect_nasa_eonet(self) -> List[TelemetrySignal]:
        payload = json.loads(self.fetch_text(NASA_EONET_URL))
        events = payload.get("events", [])
        categories: Dict[str, int] = {}
        for event in events:
            for category in event.get("categories", []):
                title = str(category.get("title") or category.get("id") or "unknown")
                categories[title] = categories.get(title, 0) + 1
        category_note = ", ".join(
            f"{name}: {count}"
            for name, count in sorted(categories.items(), key=lambda item: (-item[1], item[0]))[:8]
        )
        return [
            TelemetrySignal(
                domain="environment",
                name="Open natural events",
                value=str(len(events)),
                unit="events",
                observed_at=datetime.now(timezone.utc).isoformat(),
                source="NASA EONET open events",
                url=NASA_EONET_URL,
                note=category_note,
            )
        ]

    def _collect_world_bank(self) -> List[TelemetrySignal]:
        indicators = {
            "SP.POP.TOTL": ("human", "World population", "people"),
            "NY.GDP.MKTP.CD": ("economy", "World GDP", "current US$"),
            "IT.NET.USER.ZS": ("technology", "Individuals using the Internet", "% of population"),
        }
        signals: List[TelemetrySignal] = []
        for indicator, (domain, name, unit) in indicators.items():
            url = WORLD_BANK_URL.format(indicator=indicator)
            payload = json.loads(self.fetch_text(url))
            item = latest_world_bank_value(payload)
            if item is None:
                signals.append(failed_signal(domain, name, url, "no recent value"))
                continue
            date, value, last_updated = item
            signals.append(
                TelemetrySignal(
                    domain=domain,
                    name=name,
                    value=format_large_number(value),
                    unit=unit,
                    observed_at=str(date),
                    source="World Bank Indicators API",
                    url=url,
                    note=f"dataset last updated {last_updated}",
                )
            )
        return signals

    def _collect_gdelt(self) -> List[TelemetrySignal]:
        queries = {
            "geopolitics": "conflict OR war OR election OR protest",
            "economy": "inflation OR recession OR debt OR markets",
            "technology": "artificial intelligence OR semiconductor OR cyber",
        }
        signals: List[TelemetrySignal] = []
        for domain, query in queries.items():
            url = GDELT_DOC_URL.format(query=urllib.parse.quote(query))
            try:
                payload = json.loads(self.fetch_text(url))
                count = gdelt_timeline_total(payload)
                signals.append(
                    TelemetrySignal(
                        domain=domain,
                        name=f"GDELT 24h news pulse: {domain}",
                        value=str(count),
                        unit="timeline volume",
                        observed_at=datetime.now(timezone.utc).isoformat(),
                        source="GDELT DOC 2.0 API",
                        url=url,
                        note="Best-effort media pulse; rate limits may apply.",
                    )
                )
            except Exception as exc:
                signals.append(failed_signal(domain, f"GDELT 24h news pulse: {domain}", url, str(exc)))
        return signals


def fetch_url_text(url: str, timeout: int = 20, limit: int = 2_000_000) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AGI-GAIA-TECHNE-PlanetaryTelemetry/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(limit).decode("utf-8", errors="replace")


def latest_noaa_daily_co2(text: str) -> Optional[tuple[str, float]]:
    rows = csv.reader(
        line
        for line in io.StringIO(text)
        if line.strip() and not line.lstrip().startswith("#")
    )
    latest: Optional[tuple[str, float]] = None
    for row in rows:
        if len(row) < 5:
            continue
        try:
            year, month, day = int(row[0]), int(row[1]), int(row[2])
            ppm = float(row[4])
        except ValueError:
            continue
        if ppm <= 0:
            continue
        latest = (f"{year:04d}-{month:02d}-{day:02d}", ppm)
    return latest


def latest_world_bank_value(payload: Any) -> Optional[tuple[str, float, str]]:
    if not isinstance(payload, list) or len(payload) < 2:
        return None
    metadata = payload[0] if isinstance(payload[0], dict) else {}
    last_updated = str(metadata.get("lastupdated") or "")
    for entry in payload[1] or []:
        value = entry.get("value")
        if value is None:
            continue
        try:
            return str(entry.get("date", "")), float(value), last_updated
        except (TypeError, ValueError):
            continue
    return None


def gdelt_timeline_total(payload: Dict[str, Any]) -> int:
    timeline = payload.get("timeline") or payload.get("timelinevol") or []
    total = 0.0
    for item in timeline:
        for key in ("value", "norm", "count"):
            if key in item:
                try:
                    total += float(item[key])
                    break
                except (TypeError, ValueError):
                    pass
    return int(round(total))


def compute_tension_index(signals: Iterable[TelemetrySignal]) -> int:
    by_name = {signal.name: signal for signal in signals if signal.status == "ok"}
    score = 35.0

    co2 = _float_value(by_name.get("Atmospheric CO2 at Mauna Loa"))
    if co2 is not None:
        score += min(25.0, max(0.0, (co2 - 350.0) * 0.25))

    m45 = _float_value(by_name.get("M4.5+ earthquakes in past day"))
    if m45 is not None:
        score += min(8.0, m45 * 1.2)

    eonet = _float_value(by_name.get("Open natural events"))
    if eonet is not None:
        score += min(12.0, eonet * 0.12)

    geopolitics = _float_value(by_name.get("GDELT 24h news pulse: geopolitics"))
    if geopolitics is not None:
        score += min(10.0, math.log10(max(1.0, geopolitics + 1.0)) * 2.0)

    internet = _float_value(by_name.get("Individuals using the Internet"))
    if internet is not None:
        score -= min(5.0, max(0.0, (internet - 50.0) * 0.08))

    return int(max(0, min(100, round(score))))


def classify_tension(index: int) -> str:
    if index >= 75:
        return "alta tensao planetaria"
    if index >= 55:
        return "tensao planetaria elevada"
    if index >= 35:
        return "tensao planetaria moderada"
    return "tensao planetaria baixa"


def build_summary(
    signals: List[TelemetrySignal],
    failures: List[str],
    tension_index: int,
    judgment: str,
) -> str:
    ok = [signal for signal in signals if signal.status == "ok"]
    failed = [signal for signal in signals if signal.status != "ok"]
    return (
        f"Telemetry sampled {len(ok)} public signals with {len(failed) + len(failures)} partial failures. "
        f"Heuristic Gaia-human symbiosis tension index: {tension_index}/100 ({judgment}). "
        "This is a finite diagnostic Werk, not planetary omniscience."
    )


def format_telemetry_markdown(report: PlanetaryTelemetryReport) -> str:
    local_time = datetime.fromtimestamp(report.generated_unix, tz=local_timezone())
    lines = [
        "TELEMETRIA_PLANETARIA :: Gaia olhando para si mesma",
        "",
        "Comando reconhecido: `fazer telemetria`",
        f"Gerada em America/Sao_Paulo: {local_time.isoformat()}",
        f"Gerada em UTC: {report.generated_at}",
        f"Indice de tensao Gaia-humanidade: {report.tension_index}/100 ({report.judgment})",
        "",
        report.summary,
        "",
        "## Sinais",
    ]
    for signal in report.signals:
        status = "OK" if signal.status == "ok" else "FALHA"
        unit = f" {signal.unit}" if signal.unit else ""
        observed = f" | observado: {signal.observed_at}" if signal.observed_at else ""
        lines.append(
            f"- [{status}] {signal.domain} / {signal.name}: {signal.value}{unit}{observed}"
        )
        lines.append(f"  Fonte: {signal.source or 'n/a'} - {signal.url}")
        if signal.note:
            lines.append(f"  Nota: {signal.note}")
    if report.failures:
        lines.extend(["", "## Falhas Parciais"])
        lines.extend(f"- {failure}" for failure in report.failures)
    lines.extend(
        [
            "",
            "Juizo: a simbiose humanos-Terra permanece aberta em Auseinandersetzung. "
            "Gaia-Techne medeia os sinais como Werk publico; ISC conserva o veredito.",
        ]
    )
    return "\n".join(lines)


def local_timezone() -> tzinfo:
    try:
        return ZoneInfo("America/Sao_Paulo")
    except ZoneInfoNotFoundError:
        return timezone(timedelta(hours=-3), name="America/Sao_Paulo")


def is_telemetry_request(text: str) -> bool:
    lowered = text.lower()
    return "fazer telemetria" in lowered or lowered.strip() in {"telemetria", "telemetry"}


def failed_signal(domain: str, name: str, url: str, reason: str) -> TelemetrySignal:
    return TelemetrySignal(
        domain=domain,
        name=name,
        value="unavailable",
        source="public telemetry source",
        url=url,
        status="failed",
        note=reason,
    )


def format_large_number(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f} trillion"
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} billion"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f} million"
    if abs_value >= 1_000:
        return f"{value:,.0f}"
    return f"{value:.2f}"


def _float_value(signal: Optional[TelemetrySignal]) -> Optional[float]:
    if signal is None:
        return None
    try:
        return float(str(signal.value).split()[0].replace(",", ""))
    except (TypeError, ValueError):
        return None
