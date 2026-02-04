"""Text tools - diff, regex, word count."""

import re
from cacao.core.state import State

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
    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Text Diff"}},
                            {"type": "p", "props": {"content": "Compare two texts and see the differences"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "div",
                                "props": {
                                    "className": "dual-pane",
                                    "children": [
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Original Text"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "placeholder": "Enter original text...",
                                                            "value": diff_text1.value,
                                                            "onChange": "diff:text1",
                                                            "className": "tool-input mono",
                                                            "rows": 10
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Modified Text"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "placeholder": "Enter modified text...",
                                                            "value": diff_text2.value,
                                                            "onChange": "diff:text2",
                                                            "className": "tool-input mono",
                                                            "rows": 10
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "button",
                                "props": {
                                    "content": "Compare",
                                    "onClick": "diff:compare",
                                    "className": "btn btn-primary"
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "diff-output",
                                    "children": _render_diff_result()
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _render_diff_result():
    """Render the diff result."""
    if not diff_result.value:
        return []

    children = []
    for item in diff_result.value:
        line_class = "diff-line"
        if item["type"] == "add":
            line_class += " diff-add"
            prefix = "+ "
        elif item["type"] == "remove":
            line_class += " diff-remove"
            prefix = "- "
        else:
            prefix = "  "

        children.append({
            "type": "div",
            "props": {
                "className": line_class,
                "content": prefix + item["text"]
            }
        })

    return children


def regex_tester():
    """Regular expression tester."""
    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Regex Tester"}},
                            {"type": "p", "props": {"content": "Test regular expressions against sample text"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "div",
                                "props": {
                                    "className": "regex-input-group",
                                    "children": [
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "regex-pattern",
                                                "children": [
                                                    {"type": "span", "props": {"content": "/", "className": "regex-delimiter"}},
                                                    {
                                                        "type": "input",
                                                        "props": {
                                                            "type": "text",
                                                            "placeholder": "Enter regex pattern...",
                                                            "value": regex_pattern.value,
                                                            "onChange": "regex:pattern",
                                                            "className": "regex-input mono"
                                                        }
                                                    },
                                                    {"type": "span", "props": {"content": "/", "className": "regex-delimiter"}},
                                                    {"type": "span", "props": {"content": _get_flags_string(), "className": "regex-flags"}}
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "regex-flags-group",
                                    "children": [
                                        _flag_checkbox("i", "Case insensitive", regex_flags.value.get("i", False)),
                                        _flag_checkbox("m", "Multiline", regex_flags.value.get("m", False)),
                                        _flag_checkbox("g", "Global", regex_flags.value.get("g", True)),
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "test-text-section",
                                    "children": [
                                        {"type": "label", "props": {"content": "Test String"}},
                                        {
                                            "type": "textarea",
                                            "props": {
                                                "placeholder": "Enter text to test against...",
                                                "value": regex_text.value,
                                                "onChange": "regex:text",
                                                "className": "tool-input mono",
                                                "rows": 6
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "match-results",
                                    "children": [
                                        {"type": "h4", "props": {"content": f"Matches ({len(regex_matches.value)})"}},
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "matches-list",
                                                "children": _render_matches()
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


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


def _flag_checkbox(flag: str, label: str, checked: bool):
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
                {"type": "span", "props": {"content": f"{flag} - {label}"}}
            ]
        }
    }


def _render_matches():
    """Render regex matches."""
    if not regex_matches.value:
        return [{"type": "p", "props": {"content": "No matches found", "className": "no-matches"}}]

    return [
        {
            "type": "div",
            "props": {
                "className": "match-item",
                "children": [
                    {"type": "span", "props": {"content": f"Match {i+1}:", "className": "match-index"}},
                    {"type": "span", "props": {"content": match, "className": "match-text mono"}}
                ]
            }
        }
        for i, match in enumerate(regex_matches.value)
    ]


def word_counter():
    """Word/character counter tool."""
    stats = wc_stats.value

    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Word Counter"}},
                            {"type": "p", "props": {"content": "Count words, characters, lines, and sentences"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "textarea",
                                "props": {
                                    "placeholder": "Enter or paste your text here...",
                                    "value": wc_input.value,
                                    "onChange": "wc:input",
                                    "className": "tool-input",
                                    "rows": 10
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "stats-grid",
                                    "children": [
                                        _stat_card("Words", stats.get("words", 0), "fa-solid fa-font"),
                                        _stat_card("Characters", stats.get("chars", 0), "fa-solid fa-text-width"),
                                        _stat_card("No Spaces", stats.get("chars_no_space", 0), "fa-solid fa-minus"),
                                        _stat_card("Lines", stats.get("lines", 0), "fa-solid fa-list"),
                                        _stat_card("Sentences", stats.get("sentences", 0), "fa-solid fa-paragraph"),
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _stat_card(label: str, value: int, icon: str):
    """Render a stat card."""
    return {
        "type": "div",
        "props": {
            "className": "stat-card",
            "children": [
                {"type": "i", "props": {"className": icon}},
                {"type": "div", "props": {"className": "stat-value", "content": str(value)}},
                {"type": "div", "props": {"className": "stat-label", "content": label}}
            ]
        }
    }


# Utility functions
def simple_diff(text1: str, text2: str) -> list:
    """Simple line-by-line diff."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    result = []

    # Simple comparison - could be improved with proper diff algorithm
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
