"""Generator tools - Lorem Ipsum, QR codes."""

import random
from cacao.core.state import State

# Lorem ipsum state
lorem_paragraphs = State(3)
lorem_output = State("")

# QR code state
qr_input = State("")
qr_size = State(200)

# Lorem ipsum words
LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum"
]


def lorem_ipsum():
    """Lorem Ipsum generator."""
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
                            {"type": "h2", "props": {"content": "Lorem Ipsum Generator"}},
                            {"type": "p", "props": {"content": "Generate placeholder text for your designs"}}
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
                                    "className": "input-group",
                                    "children": [
                                        {"type": "label", "props": {"content": f"Paragraphs: {lorem_paragraphs.value}"}},
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "range",
                                                "min": 1,
                                                "max": 10,
                                                "value": lorem_paragraphs.value,
                                                "onChange": "lorem:paragraphs"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "button",
                                "props": {
                                    "content": "Generate",
                                    "onClick": "lorem:generate",
                                    "className": "btn btn-primary"
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "output-section",
                                    "children": [
                                        {
                                            "type": "textarea",
                                            "props": {
                                                "value": lorem_output.value,
                                                "readOnly": True,
                                                "className": "tool-input",
                                                "rows": 12
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Copy",
                                                "onClick": f"copy:{lorem_output.value[:100]}...",
                                                "className": "btn btn-sm"
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


def qr_code():
    """QR Code generator."""
    # Using a QR code API for simplicity
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={qr_size.value}x{qr_size.value}&data={qr_input.value}" if qr_input.value else ""

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
                            {"type": "h2", "props": {"content": "QR Code Generator"}},
                            {"type": "p", "props": {"content": "Generate QR codes for URLs, text, or any data"}}
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
                                    "className": "input-section",
                                    "children": [
                                        {"type": "label", "props": {"content": "Content"}},
                                        {
                                            "type": "textarea",
                                            "props": {
                                                "placeholder": "Enter URL or text for QR code...",
                                                "value": qr_input.value,
                                                "onChange": "qr:input",
                                                "className": "tool-input",
                                                "rows": 3
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "input-group",
                                    "children": [
                                        {"type": "label", "props": {"content": f"Size: {qr_size.value}px"}},
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "range",
                                                "min": 100,
                                                "max": 400,
                                                "step": 50,
                                                "value": qr_size.value,
                                                "onChange": "qr:size"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "qr-preview",
                                    "children": [
                                        {
                                            "type": "img",
                                            "props": {
                                                "src": qr_url,
                                                "alt": "QR Code",
                                                "className": "qr-image"
                                            }
                                        } if qr_url else {
                                            "type": "div",
                                            "props": {
                                                "className": "qr-placeholder",
                                                "children": [
                                                    {"type": "p", "props": {"content": "Enter content to generate QR code"}}
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "a",
                                "props": {
                                    "href": qr_url,
                                    "download": "qrcode.png",
                                    "className": "btn btn-primary",
                                    "content": "Download QR Code"
                                }
                            } if qr_url else {"type": "span", "props": {}}
                        ]
                    }
                }
            ]
        }
    }


# Utility functions
def generate_sentence() -> str:
    """Generate a random lorem ipsum sentence."""
    length = random.randint(8, 15)
    words = [random.choice(LOREM_WORDS) for _ in range(length)]
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'


def generate_paragraph() -> str:
    """Generate a random lorem ipsum paragraph."""
    sentences = [generate_sentence() for _ in range(random.randint(4, 8))]
    return ' '.join(sentences)


def generate_lorem(num_paragraphs: int) -> str:
    """Generate lorem ipsum text with specified number of paragraphs."""
    paragraphs = [generate_paragraph() for _ in range(num_paragraphs)]
    # Always start with "Lorem ipsum dolor sit amet"
    if paragraphs:
        paragraphs[0] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " + paragraphs[0]
    return '\n\n'.join(paragraphs)
