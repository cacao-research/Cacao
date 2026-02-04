"""Generator tools - Lorem Ipsum, QR codes."""

import random
import urllib.parse
from cacao.core.state import State
from cacao.ui import (
    div, p, button, textarea, label, img,
    tool_container, labeled, range_input, link
)

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

# Sentence length range
SENTENCE_MIN_WORDS = 8
SENTENCE_MAX_WORDS = 15
SENTENCES_PER_PARAGRAPH_MIN = 4
SENTENCES_PER_PARAGRAPH_MAX = 8


def lorem_ipsum():
    """Lorem Ipsum generator."""
    return tool_container(
        "Lorem Ipsum Generator",
        "Generate placeholder text for your designs",
        labeled(
            f"Paragraphs: {lorem_paragraphs.value}",
            range_input(
                value=lorem_paragraphs.value,
                onChange="lorem:paragraphs",
                min=1,
                max=10
            )
        ),
        button("Generate", onClick="lorem:generate", className="btn btn-primary"),
        div(
            textarea(
                value=lorem_output.value,
                readOnly=True,
                className="tool-input",
                rows=12
            ),
            button("Copy", onClick=f"copy:{lorem_output.value}", className="btn btn-sm"),
            className="output-section"
        )
    )


def qr_code():
    """QR Code generator."""
    # URL-encode the input for the QR API
    encoded_data = urllib.parse.quote(qr_input.value, safe='') if qr_input.value else ""
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={qr_size.value}x{qr_size.value}&data={encoded_data}" if qr_input.value else ""

    return tool_container(
        "QR Code Generator",
        "Generate QR codes for URLs, text, or any data",
        div(
            label("Content"),
            textarea(
                value=qr_input.value,
                onChange="qr:input",
                placeholder="Enter URL or text for QR code...",
                className="tool-input",
                rows=3
            ),
            className="input-section"
        ),
        labeled(
            f"Size: {qr_size.value}px",
            range_input(
                value=qr_size.value,
                onChange="qr:size",
                min=100,
                max=400,
                step=50
            )
        ),
        div(
            img(src=qr_url, alt="QR Code", className="qr-image") if qr_url else
            div(p("Enter content to generate QR code"), className="qr-placeholder"),
            className="qr-preview"
        ),
        link("Download QR Code", href=qr_url, download="qrcode.png", className="btn btn-primary") if qr_url else
        {"type": "span", "props": {}}
    )


# Utility functions

def generate_sentence() -> str:
    """Generate a random lorem ipsum sentence."""
    length = random.randint(SENTENCE_MIN_WORDS, SENTENCE_MAX_WORDS)
    words = [random.choice(LOREM_WORDS) for _ in range(length)]
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'


def generate_paragraph() -> str:
    """Generate a random lorem ipsum paragraph."""
    num_sentences = random.randint(SENTENCES_PER_PARAGRAPH_MIN, SENTENCES_PER_PARAGRAPH_MAX)
    sentences = [generate_sentence() for _ in range(num_sentences)]
    return ' '.join(sentences)


def generate_lorem(num_paragraphs: int) -> str:
    """Generate lorem ipsum text with specified number of paragraphs."""
    paragraphs = [generate_paragraph() for _ in range(num_paragraphs)]
    # Always start with "Lorem ipsum dolor sit amet"
    if paragraphs:
        paragraphs[0] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " + paragraphs[0]
    return '\n\n'.join(paragraphs)
