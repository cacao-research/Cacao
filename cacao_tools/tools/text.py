"""Text tools - diff, regex, word count."""

import re
from cacao.core.state import State
from cacao.ui import (
    div, h4, p, span, button, textarea, label, input, checkbox,
    tool_container, dual_pane, stat_card
)

# Text diff state
diff_text1 = State("")
diff_text2 = State("")
diff_result = State([])

# Regex state
regex_pattern = State("")
regex_text = State("")
regex_matches = State([])
regex_flags = State({"i": False, "m": False, "g": True})

# Word counter state
wc_input = State("")
wc_stats = State({"chars": 0, "chars_no_space": 0, "words": 0, "lines": 0, "sentences": 0})


def text_diff():
    """Text comparison/diff tool."""
    return tool_container(
        "Text Diff",
        "Compare two texts and see the differences",
        dual_pane(
            "Original Text",
            textarea(
                value=diff_text1.value,
                onChange="diff:text1",
                placeholder="Enter original text...",
                className="tool-input mono",
                rows=10
            ),
            "Modified Text",
            textarea(
                value=diff_text2.value,
                onChange="diff:text2",
                placeholder="Enter modified text...",
                className="tool-input mono",
                rows=10
            )
        ),
        button("Compare", onClick="diff:compare", className="btn btn-primary"),
        div(*_render_diff_result(), className="diff-output")
    )


def _render_diff_result():
    """Render the diff result."""
    if not diff_result.value:
        return []

    children = []
    for item in diff_result.value:
        if item["type"] == "add":
            line_class = "diff-line diff-add"
            prefix = "+ "
        elif item["type"] == "remove":
            line_class = "diff-line diff-remove"
            prefix = "- "
        else:
            line_class = "diff-line"
            prefix = "  "

        children.append(div(prefix + item["text"], className=line_class))

    return children


def _get_flags_string() -> str:
    """Get flags string for display."""
    flags = ""
    if regex_flags.value.get("g"):
        flags += "g"
    if regex_flags.value.get("i"):
        flags += "i"
    if regex_flags.value.get("m"):
        flags += "m"
    return flags


def _flag_checkbox(flag: str, label_text: str, checked: bool):
    """Render a regex flag checkbox."""
    return {
        "type": "label",
        "props": {
            "className": "flag-checkbox",
            "children": [
                {
                    "type": "input",
                    "props": {
                        "type": "checkbox",
                        "checked": checked,
                        "onChange": f"regex:flag:{flag}"
                    }
                },
                span(f"{flag} - {label_text}")
            ]
        }
    }


def _render_matches():
    """Render regex matches."""
    if not regex_matches.value:
        return [p("No matches found", className="no-matches")]

    return [
        div(
            span(f"Match {i+1}:", className="match-index"),
            span(match, className="match-text mono"),
            className="match-item"
        )
        for i, match in enumerate(regex_matches.value)
    ]


def regex_tester():
    """Regular expression tester."""
    return tool_container(
        "Regex Tester",
        "Test regular expressions against sample text",
        div(
            div(
                span("/", className="regex-delimiter"),
                input(
                    value=regex_pattern.value,
                    onChange="regex:pattern",
                    placeholder="Enter regex pattern...",
                    className="regex-input mono"
                ),
                span("/", className="regex-delimiter"),
                span(_get_flags_string(), className="regex-flags"),
                className="regex-pattern"
            ),
            className="regex-input-group"
        ),
        div(
            _flag_checkbox("i", "Case insensitive", regex_flags.value.get("i", False)),
            _flag_checkbox("m", "Multiline", regex_flags.value.get("m", False)),
            _flag_checkbox("g", "Global", regex_flags.value.get("g", True)),
            className="regex-flags-group"
        ),
        div(
            label("Test String"),
            textarea(
                value=regex_text.value,
                onChange="regex:text",
                placeholder="Enter text to test against...",
                className="tool-input mono",
                rows=6
            ),
            className="test-text-section"
        ),
        div(
            h4(f"Matches ({len(regex_matches.value)})"),
            div(*_render_matches(), className="matches-list"),
            className="match-results"
        )
    )


def word_counter():
    """Word/character counter tool."""
    stats = wc_stats.value

    return tool_container(
        "Word Counter",
        "Count words, characters, lines, and sentences",
        textarea(
            value=wc_input.value,
            onChange="wc:input",
            placeholder="Enter or paste your text here...",
            className="tool-input",
            rows=10
        ),
        div(
            stat_card("Words", stats.get("words", 0), "fa-solid fa-font"),
            stat_card("Characters", stats.get("chars", 0), "fa-solid fa-text-width"),
            stat_card("No Spaces", stats.get("chars_no_space", 0), "fa-solid fa-minus"),
            stat_card("Lines", stats.get("lines", 0), "fa-solid fa-list"),
            stat_card("Sentences", stats.get("sentences", 0), "fa-solid fa-paragraph"),
            className="stats-grid"
        )
    )


# Utility functions

def simple_diff(text1: str, text2: str) -> list:
    """Simple line-by-line diff."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    result = []
    max_len = max(len(lines1), len(lines2))

    for i in range(max_len):
        line1 = lines1[i] if i < len(lines1) else None
        line2 = lines2[i] if i < len(lines2) else None

        if line1 == line2:
            result.append({"type": "same", "text": line1 or ""})
        else:
            if line1 is not None:
                result.append({"type": "remove", "text": line1})
            if line2 is not None:
                result.append({"type": "add", "text": line2})

    return result


def test_regex(pattern: str, text: str, flags: dict) -> list:
    """Test regex pattern against text."""
    try:
        re_flags = 0
        if flags.get("i"):
            re_flags |= re.IGNORECASE
        if flags.get("m"):
            re_flags |= re.MULTILINE

        compiled = re.compile(pattern, re_flags)

        if flags.get("g"):
            return compiled.findall(text)
        else:
            match = compiled.search(text)
            return [match.group()] if match else []
    except re.error:
        return []


def count_text(text: str) -> dict:
    """Count various text statistics."""
    if not text:
        return {"chars": 0, "chars_no_space": 0, "words": 0, "lines": 0, "sentences": 0}

    return {
        "chars": len(text),
        "chars_no_space": len(text.replace(" ", "").replace("\n", "").replace("\t", "")),
        "words": len(text.split()),
        "lines": len(text.splitlines()) or 1,
        "sentences": len(re.findall(r'[.!?]+', text))
    }
