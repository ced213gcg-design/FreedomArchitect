from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONT = ROOT / "19_Live_Adaptive_Dashboard" / "frontend"


def read(name):
    return (FRONT / name).read_text(encoding="utf-8")


def test_horizon_and_command_deck_are_always_recoverable():
    html = read("index.html")
    horizon = read("ccc_horizon.js")
    deck = read("command_deck.js")
    assert 'id="horizon"' in html
    assert 'data-ccc-home' in html
    assert 'id="commandDeck"' in html
    assert "event.key.toLowerCase()==='h'" in horizon
    assert "event.key.toLowerCase()==='d'" in deck


def test_context_lens_embeds_ccc_three_and_six_plus_raw_evidence():
    html = read("index.html")
    lens = read("context_lens.js")
    assert 'VIEW RAW EVIDENCE' in html
    for field in ["STATE", "FACT", "RISK", "NEXT ACTION", "OWNER", "SOURCE", "TIME", "VALIDATION", "APPROVAL"]:
        assert field in lens
    assert "JSON.stringify(data,null,2)" in lens


def test_focus_and_reduced_motion_are_explicit():
    css = read("ccc_multiverse.css")
    cards = read("object_cards.js")
    assert ":focus-visible" in css
    assert "prefers-reduced-motion:reduce" in css
    assert "article.tabIndex=0" in cards
    assert "e.key==='Enter'||e.key===' '" in cards


def test_no_remote_cdn_or_font_dependency_added():
    html = read("index.html")
    lowered = html.lower()
    assert "fonts.googleapis.com" not in lowered
    assert "cdn.jsdelivr.net" not in lowered
    assert "unpkg.com" not in lowered


def test_soc_request_is_preview_not_direct_execution():
    cards = read("object_cards.js")
    lens = read("context_lens.js")
    assert "previewAction" in cards
    assert "REQUEST_SOC_TEST" in cards
    assert "Confirmation does not execute the underlying action" in lens
