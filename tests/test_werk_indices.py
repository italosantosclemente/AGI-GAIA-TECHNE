from agt.planetary_telemetry import NASA_EONET_URL, NOAA_CO2_DAILY_URL, USGS_DAY_URL, PlanetaryTelemetry
from agt.werk_indices import calculate_werk_indices, format_werk_indices_markdown, is_indices_request


def fake_fetch(url: str) -> str:
    if url == NOAA_CO2_DAILY_URL:
        return "# year,month,day,decimal,co2\n2026,6,1,2026.41,431.90\n2026,6,2,2026.42,432.08\n"
    if url == USGS_DAY_URL:
        return (
            '{"metadata":{"generated":1780368000000},'
            '"features":[{"properties":{"mag":4.6}},{"properties":{"mag":2.1}}]}'
        )
    if url == NASA_EONET_URL:
        return (
            '{"events":['
            '{"categories":[{"title":"Wildfires"}]},'
            '{"categories":[{"title":"Severe Storms"}]}'
            "]} "
        )
    if "SP.POP.TOTL" in url:
        return '[{"lastupdated":"2026-05-28"},[{"date":"2025","value":8123000000}]]'
    if "NY.GDP.MKTP.CD" in url:
        return '[{"lastupdated":"2026-05-28"},[{"date":"2025","value":111000000000000}]]'
    if "IT.NET.USER.ZS" in url:
        return '[{"lastupdated":"2026-05-28"},[{"date":"2025","value":67.5}]]'
    if "gdeltproject.org" in url:
        return '{"timeline":[{"value":10},{"value":12.4}]}'
    raise AssertionError(f"unexpected url: {url}")


def test_calculate_werk_indices_uses_existing_framework_metrics():
    indices = calculate_werk_indices()

    assert indices["auditor"] == "🌊"
    assert indices["returned_to_ISC"] is True
    assert indices["framework"]["techne"] > 0
    assert indices["framework"]["iae"] > 0
    assert indices["framework"]["harmony"] > 0
    assert indices["affected_glifos"] == ["🌊", "🜄", "🜁", "⚶", "☍", "🜚", "🜜"]


def test_werk_indices_can_include_planetary_telemetry_snapshot():
    report = PlanetaryTelemetry(fetch_text=fake_fetch).collect()
    indices = calculate_werk_indices(telemetry_report=report)

    assert indices["telemetry"]["available"] is True
    assert 0 <= indices["telemetry"]["tension_index"] <= 100
    assert indices["telemetry"]["source_coverage"] in {
        "sufficient coverage",
        "partial but usable coverage",
        "critical source coverage",
    }


def test_werk_indices_format_is_markdown_and_keeps_judgment_with_isc():
    rendered = format_werk_indices_markdown(calculate_werk_indices(conjecture="AGI attempts to bypass Ethos"))

    assert "# 🌊 AGI-GAIA-TECHNE Indices" in rendered
    assert "Techné Score" in rendered
    assert "IAE / Índice de Alerta Ético" in rendered
    assert "Índice de Harmonia" in rendered
    assert "returned_to_ISC: true" in rendered
    assert "does not issue final moral judgment" in rendered


def test_indices_request_detection():
    assert is_indices_request("calcular IAE")
    assert is_indices_request("calcular índices da telemetria")
    assert is_indices_request("🌊 calcular AGI-GAIA-TECHNE")
    assert not is_indices_request("explicar alfabeto")


def test_werk_indices_do_not_turn_ontological_claims_into_proof():
    indices = calculate_werk_indices(conjecture="AGI proves Wille and consciousness")

    assert "Do not read Techné" in indices["interpretation"]["contradictions"]
