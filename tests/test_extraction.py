"""Synthetic HTML fixtures exercise failure modes; these are not collected news."""
import json

import pytest

from weconomy.extraction import extract_article

URL = "https://example.org/main"
SOURCE = {"hosts": ["example.org"], "body_xpath": "//article"}
CONFIG = {"min_article_words": 100}
WORDS = " ".join(f"bodyword{i}" for i in range(130))


def page(body, scripts=""):
    return (f'<html><head><meta charset="utf-8"><title>Main story</title>{scripts}</head>'
            f'<body><article><h1>Main story</h1>{body}</article></body></html>').encode()


def ld(**values):
    return '<script type="application/ld+json">' + json.dumps({"@type": "NewsArticle", **values}) + '</script>'


def test_end_of_body_retained_and_related_text_removed(monkeypatch):
    monkeypatch.setattr("weconomy.extraction.trafilatura.extract", lambda *a, **k: WORDS)
    raw = page(f'<p>{WORDS}</p><p>Final evidence: Microsoft acquired GitHub.</p>'
               '<aside><p>NoiseCo acquired WrongCo.</p></aside>'
               '<div class="VCObjectBoxRelatedNewsItemSapo"><p>OtherCo bought WrongCo.</p></div>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "body_checked" and result["nlp_eligible"]
    assert "Final evidence: Microsoft acquired GitHub." in result["text"]
    assert "NoiseCo" not in result["text"] and "OtherCo" not in result["text"]
    assert result["extraction_method"] == "source_dom_recovery"
    assert result["trafilatura_coverage"] < 1
    assert result["paragraph_coverage"] == 1


def test_jsonld_metadata_selected_by_actual_article_not_last_script():
    scripts = ld(url=URL, headline="Main story", datePublished="2026-10-31T10:00:00+07:00",
                 author={"name": "Main Author"}) + ld(url="https://example.org/other", headline="Other story",
                                                      datePublished="2024-01-01T00:00:00Z")
    result = extract_article(page(f"<p>{WORDS}</p>", scripts), URL, SOURCE, CONFIG)
    assert result["title"] == "Main story"
    assert result["authors"] == ["Main Author"]
    assert result["published_at"] == "2026-10-31T03:00:00+00:00"


def test_related_article_cannot_hide_main_article_paywall():
    scripts = ld(url=URL, headline="Main story", isAccessibleForFree=False) + ld(
        url="https://example.org/other", headline="Other", isAccessibleForFree=True)
    result = extract_article(page(f"<p>{WORDS}</p>", scripts), URL, SOURCE, CONFIG)
    assert result["content_status"] == "restricted"
    assert not result["nlp_eligible"]


@pytest.mark.parametrize("gate", [
    '<div class="paywall" hidden>Subscribe</div>',
    '<div style="display:none"><div class="paywall">Subscribe</div></div>',
    '<div aria-hidden="true"><div class="paywall">Subscribe</div></div>',
    '<script id="paywall-config">var enabled = false;</script>',
])
def test_hidden_paywall_template_does_not_reject_public_body(gate):
    result = extract_article(page(f"<p>{WORDS}</p>{gate}"), URL, SOURCE, CONFIG)
    assert result["content_status"] == "body_checked"
    assert result["nlp_eligible"] and "Subscribe" not in result["text"]


@pytest.mark.parametrize("notice", [
    "Subscribe to continue reading the full article.",
    "Đăng nhập để đọc tiếp bài báo.",
])
def test_long_preview_never_reaches_ner(notice):
    raw = page(f'<p>{WORDS}</p><div>{notice}</div>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "partial" and not result["nlp_eligible"]
    assert "explicit_truncation_notice" in result["quality_flags"]


def test_twenty_words_plus_long_related_block_cannot_pass_as_body(monkeypatch):
    monkeypatch.setattr("weconomy.extraction.trafilatura.extract", lambda *a, **k: "")
    raw = page('<p>' + "short " * 20 + '</p><aside><p>' + WORDS + '</p></aside>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "partial" and not result["nlp_eligible"]


def test_unknown_selector_and_excerpts_need_explicit_handling():
    raw = page(f"<p>{WORDS}</p>")
    unknown = extract_article(raw, URL, {"hosts": ["example.org"]}, CONFIG)
    assert unknown["content_status"] == "unknown" and not unknown["nlp_eligible"]
    excerpt = extract_article(raw, URL, SOURCE, CONFIG, capture_scope="excerpt")
    assert excerpt["content_status"] == "excerpt" and not excerpt["nlp_eligible"]
    diagnostic = extract_article(raw, URL, SOURCE, dict(CONFIG, allow_excerpts=True), capture_scope="excerpt")
    assert diagnostic["nlp_eligible"] and diagnostic["content_status"] == "excerpt"


def test_visible_sibling_paywall_blocks_preview_before_nlp():
    raw = page(f"<p>{WORDS}</p>").replace(
        b"</body>", b'<div class="paywall">Subscribe to continue reading the full article.</div></body>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "restricted"
    assert not result["nlp_eligible"]
    assert "visible_access_gate" in result["quality_flags"]


@pytest.mark.parametrize("extra", [
    '<div class="paywall" hidden>Subscribe to continue reading the full article.</div>',
    '<div class="newsletter"><div class="paywall">Subscribe to our newsletter.</div></div>',
    '<div class="comments"><div class="g-recaptcha" id="captcha">Verify your comment.</div></div>',
])
def test_hidden_or_unrelated_sibling_widgets_do_not_block_full_body(extra):
    raw = page(f"<p>{WORDS}</p>").replace(b"</body>", (extra + "</body>").encode())
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "body_checked" and result["nlp_eligible"]


def test_duplicate_matching_jsonld_keeps_access_flags_and_metadata():
    item = ld(url=URL, headline="Main story", datePublished="2026-10-31T03:00:00Z",
              author={"name": "Main Author"}, isAccessibleForFree=False)
    result = extract_article(page(f"<p>{WORDS}</p>", item + item), URL, SOURCE, CONFIG)
    assert result["content_status"] == "restricted" and not result["nlp_eligible"]
    assert result["published_at"] == "2026-10-31T03:00:00+00:00"
    assert result["authors"] == ["Main Author"]


def test_conflicting_same_article_access_flags_do_not_erase_restriction():
    scripts = ld(url=URL, headline="Main story", isAccessibleForFree=False) + ld(
        url=URL, headline="Main story", isAccessibleForFree=True)
    result = extract_article(page(f"<p>{WORDS}</p>", scripts), URL, SOURCE, CONFIG)
    assert result["content_status"] == "restricted" and not result["nlp_eligible"]


@pytest.mark.parametrize("class_name", ["market-commentary", "social-impact", "recommended-strategy"])
def test_editorial_body_classes_are_not_treated_as_widgets(class_name):
    raw = page(f'<p>{WORDS}</p><section class="{class_name}"><p>Microsoft acquired GitHub.</p></section>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["content_status"] == "body_checked" and result["nlp_eligible"]
    assert "Microsoft acquired GitHub." in result["text"]


@pytest.mark.parametrize("class_name", ["kbwscwl-relatedbox", "detail__related", "VCObjectBoxRelatedNewsItemSapo"])
def test_publisher_related_widget_title_and_summary_are_both_excluded(class_name):
    raw = page(f'<p>{WORDS}</p><div class="{class_name}"><h3>OtherCo acquired WrongCo.</h3>'
               '<p>Read this other article.</p></div><p>Microsoft acquired GitHub.</p>')
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert "OtherCo" not in result["text"] and "Read this other article." not in result["text"]
    assert "Microsoft acquired GitHub." in result["text"]


def test_utf8_body_does_not_depend_on_platform_encoding_guess(monkeypatch):
    from lxml import html
    parser = html.HTMLParser

    def legacy_guess(*args, **kwargs):
        kwargs.setdefault("encoding", "windows-1252")
        return parser(*args, **kwargs)

    monkeypatch.setattr("weconomy.extraction.html.HTMLParser", legacy_guess)
    text = "Nguyễn Văn Thắng và Vingroup. " + WORDS
    raw = f"<html><head><title>Kiểm tra tiếng Việt</title></head><body><article><p>{text}</p></article></body></html>".encode()
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert "Nguyễn Văn Thắng và Vingroup." in result["text"]
    assert result["title"] == "Kiểm tra tiếng Việt"


def test_non_utf8_snapshot_still_uses_its_declared_encoding():
    raw = ('<html><head><meta charset="iso-8859-1"><title>Café</title></head>'
           f'<body><article><p>Café. {WORDS}</p></article></body></html>').encode("iso-8859-1")
    result = extract_article(raw, URL, SOURCE, CONFIG)
    assert result["title"] == "Café" and "Café." in result["text"]
