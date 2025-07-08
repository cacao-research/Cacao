"""
Feedback page for the components showcase.
Demonstrates feedback components like tooltip, popover, etc.
"""

class FeedbackPage:
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
                            "content": "Feedback Components",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    # Tooltip
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
                                    "type": "h3",
                                    "props": {
                                        "content": "Tooltip",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "justifyContent": "center",
                                            "marginBottom": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "tooltip",
                                                "props": {
                                                    "content": "This is a tooltip",
                                                    "placement": "top",
                                                    "children": {
                                                        "type": "button",
                                                        "props": {
                                                            "label": "Hover me",
                                                            "style": {
                                                                "backgroundColor": "#6B4226",
                                                                "color": "#FFFFFF",
                                                                "border": "none",
                                                                "borderRadius": "4px",
                                                                "padding": "8px 16px",
                                                                "cursor": "pointer"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    # Popover
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
                                    "type": "h3",
                                    "props": {
                                        "content": "Popover",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "justifyContent": "center",
                                            "marginBottom": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "popover",
                                                "props": {
                                                    "content": "This is the content of the popover. It can contain more complex content than a tooltip.",
                                                    "title": "Popover Title",
                                                    "placement": "top",
                                                    "trigger": "click",
                                                    "children": {
                                                        "type": "button",
                                                        "props": {
                                                            "label": "Click me",
                                                            "style": {
                                                                "backgroundColor": "#6B4226",
                                                                "color": "#FFFFFF",
                                                                "border": "none",
                                                                "borderRadius": "4px",
                                                                "padding": "8px 16px",
                                                                "cursor": "pointer"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    # Collapse
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
                                    "type": "h3",
                                    "props": {
                                        "content": "Collapse",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "collapse",
                                    "props": {
                                        "panels": [
                                            {
                                                "key": "1",
                                                "header": "Panel 1",
                                                "content": "Content of panel 1. You can put any content here, including other components."
                                            },
                                            {
                                                "key": "2",
                                                "header": "Panel 2",
                                                "content": "Content of panel 2. This panel is initially collapsed."
                                            },
                                            {
                                                "key": "3",
                                                "header": "Panel 3",
                                                "content": "Content of panel 3. This panel is also initially collapsed."
                                            }
                                        ],
                                        "activeKey": ["1"],
                                        "accordion": False
                                    }
                                }
                            ]
                        }
                    },
                    # Carousel
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
                                        "content": "Carousel",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "carousel",
                                    "props": {
                                        "items": [
                                            {
                                                "type": "div",
                                                "props": {
                                                    "content": "Slide 1",
                                                    "style": {
                                                        "height": "160px",
                                                        "backgroundColor": "#6B4226",
                                                        "color": "#FFFFFF",
                                                        "display": "flex",
                                                        "justifyContent": "center",
                                                        "alignItems": "center",
                                                        "fontSize": "24px"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "div",
                                                "props": {
                                                    "content": "Slide 2",
                                                    "style": {
                                                        "height": "160px",
                                                        "backgroundColor": "#8B5E41",
                                                        "color": "#FFFFFF",
                                                        "display": "flex",
                                                        "justifyContent": "center",
                                                        "alignItems": "center",
                                                        "fontSize": "24px"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "div",
                                                "props": {
                                                    "content": "Slide 3",
                                                    "style": {
                                                        "height": "160px",
                                                        "backgroundColor": "#A67C5B",
                                                        "color": "#FFFFFF",
                                                        "display": "flex",
                                                        "justifyContent": "center",
                                                        "alignItems": "center",
                                                        "fontSize": "24px"
                                                    }
                                                }
                                            }
                                        ],
                                        "autoPlay": True,
                                        "dots": True,
                                        "effect": "scrollx"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }