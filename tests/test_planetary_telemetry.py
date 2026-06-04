from agt.llm_chat import GaiaChatSession
from agt.planetary_telemetry import (
    NASA_EONET_URL,
    NOAA_CO2_DAILY_URL,
    USGS_DAY_URL,
    PlanetaryTelemetry,
    format_telemetry_markdown,
    is_telemetry_request,
)


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
            "]}"
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


def test_planetary_telemetry_collects_sourced_report():
    report = PlanetaryTelemetry(fetch_text=fake_fetch).collect()
    names = {signal.name for signal in report.signals}

    assert report.command == "fazer telemetria"
    assert "Atmospheric CO2 at Mauna Loa" in names
    assert "Earthquakes in past day" in names
    assert "Open natural events" in names
    assert "World population" in names
    assert 0 <= report.tension_index <= 100

    rendered = format_telemetry_markdown(report)
    assert "Command: `fazer telemetria`" in rendered
    assert "Gaia-humanity tension index" in rendered
    assert "Metric Guide" in rendered
    assert "Source coverage" in rendered
    assert "Source:" in rendered
    assert "ISC keeps the verdict" in rendered


def test_telemetry_command_detection():
    assert is_telemetry_request("fazer telemetria")
    assert is_telemetry_request("Por favor, fazer telemetria agora.")
    assert is_telemetry_request("telemetry")
    assert not is_telemetry_request("fazer corpus")


def test_chat_session_runs_telemetry_command_with_factory():
    report = PlanetaryTelemetry(fetch_text=fake_fetch).collect()
    session = GaiaChatSession(checkpoint_path=None, telemetry_factory=lambda: report)

    response = session.respond("fazer telemetria")

    assert "PLANETARY TELEMETRY" in response
    assert "Command: `fazer telemetria`" in response
    assert "Atmospheric CO2 at Mauna Loa" in response
