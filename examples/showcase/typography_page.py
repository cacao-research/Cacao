"""
Typography page for the components showcase.
Demonstrates headings, paragraphs, and buttons.
"""

class TypographyPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Typography Components",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h1",
                                    "props": {
                                        "content": "Heading 1",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "h2",
                                    "props": {
                                        "content": "Heading 2",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Heading 3",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "h4",
                                    "props": {
                                        "content": "Heading 4",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "h5",
                                    "props": {
                                        "content": "Heading 5",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "h6",
                                    "props": {
                                        "content": "Heading 6",
                                        "style": {"marginBottom": "10px"}
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "This is a paragraph with normal text. Paragraphs are used for blocks of text.",
                                        "style": {"marginBottom": "10px"}
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "This is another paragraph with some emphasized text.",
                                        "style": {
                                            "marginBottom": "10px",
                                            "fontStyle": "italic"
                                        }
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "This paragraph has bold text.",
                                        "style": {
                                            "marginBottom": "10px",
                                            "fontWeight": "bold"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Buttons",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "gap": "10px",
                                            "marginBottom": "10px"
                                        },
                                        "children": [
                                            {
                                                "type": "button",
                                                "props": {
                                                    "label": "Primary Button",
                                                    "style": {
                                                        "backgroundColor": "#6B4226",
                                                        "color": "#FFFFFF",
                                                        "border": "none",
                                                        "borderRadius": "4px",
                                                        "padding": "8px 16px",
                                                        "cursor": "pointer"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "button",
                                                "props": {
                                                    "label": "Secondary Button",
                                                    "style": {
                                                        "backgroundColor": "#FFFFFF",
                                                        "color": "#6B4226",
                                                        "border": "1px solid #6B4226",
                                                        "borderRadius": "4px",
                                                        "padding": "8px 16px",
                                                        "cursor": "pointer"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "button",
                                                "props": {
                                                    "label": "Disabled Button",
                                                    "style": {
                                                        "backgroundColor": "#CCCCCC",
                                                        "color": "#666666",
                                                        "border": "none",
                                                        "borderRadius": "4px",
                                                        "padding": "8px 16px",
                                                        "cursor": "not-allowed"
                                                    }
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