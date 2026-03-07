"""
Function Wrapper Recipe
=======================
Uses c.interface() to automatically generate a UI from a
plain Python function. Cacao inspects the function signature
and builds inputs, a run button, and output display.

Run: cacao run docs/cookbook/function_wrapper.py
"""

import cacao as c

c.config(title="Function Wrapper", theme="dark")

c.title("Auto-Generated Interfaces", level=1)
c.text(
    "Use c.interface() to wrap any Python function into a full UI "
    "with auto-generated inputs and output display.",
    color="dimmed",
)
c.divider()


# Example 1: Simple text tool
@c.interface
def word_counter(text: str = "Hello world") -> dict:
    """Count words, characters, and lines in text."""
    words = text.split()
    return {
        "characters": len(text),
        "words": len(words),
        "lines": text.count("\n") + 1,
        "unique_words": len(set(w.lower() for w in words)),
    }


c.spacer(size=2)


# Example 2: Math calculator
@c.interface
def compound_interest(
    principal: float = 1000.0,
    rate: float = 5.0,
    years: int = 10,
) -> dict:
    """Calculate compound interest on an investment."""
    r = rate / 100
    amount = principal * (1 + r) ** years
    interest = amount - principal
    return {
        "final_amount": f"${amount:,.2f}",
        "interest_earned": f"${interest:,.2f}",
        "total_return": f"{(amount / principal - 1) * 100:.1f}%",
    }


c.spacer(size=2)


# Example 3: Data formatter
@c.interface
def password_strength(password: str = "") -> dict:
    """Analyze password strength with simple heuristics."""
    length = len(password)
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(not ch.isalnum() for ch in password)

    score = sum([
        length >= 8,
        length >= 12,
        has_upper,
        has_lower,
        has_digit,
        has_special,
    ])

    levels = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Moderate", 4: "Strong", 5: "Very Strong", 6: "Excellent"}

    return {
        "length": length,
        "has_uppercase": has_upper,
        "has_lowercase": has_lower,
        "has_digits": has_digit,
        "has_special_chars": has_special,
        "score": f"{score}/6",
        "strength": levels.get(score, "Unknown"),
    }
