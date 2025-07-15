"""
Inputs page for the components showcase.
Demonstrates various input components like text inputs, selects, checkboxes, etc.
"""

class InputsPage:
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
                            "content": "Input Components",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    # Text Input
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
                                        "content": "Text Inputs",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "input",
                                    "props": {
                                        "inputType": "text",
                                        "placeholder": "Enter your name",
                                        "value": "",
                                        "style": {
                                            "width": "100%",
                                            "padding": "8px",
                                            "marginBottom": "10px",
                                            "borderRadius": "4px",
                                            "border": "1px solid #CCCCCC"
                                        }
                                    }
                                },
                                {
                                    "type": "input",
                                    "props": {
                                        "inputType": "password",
                                        "placeholder": "Enter your password",
                                        "value": "",
                                        "style": {
                                            "width": "100%",
                                            "padding": "8px",
                                            "marginBottom": "10px",
                                            "borderRadius": "4px",
                                            "border": "1px solid #CCCCCC"
                                        }
                                    }
                                },
                                {
                                    "type": "textarea",
                                    "props": {
                                        "placeholder": "Enter your message",
                                        "value": "",
                                        "rows": 4,
                                        "style": {
                                            "width": "100%",
                                            "padding": "8px",
                                            "marginBottom": "10px",
                                            "borderRadius": "4px",
                                            "border": "1px solid #CCCCCC"
                                        }
                                    }
                                },
                                {
                                    "type": "search",
                                    "props": {
                                        "placeholder": "Search...",
                                        "value": "",
                                        "style": {
                                            "width": "100%",
                                            "padding": "8px",
                                            "marginBottom": "10px",
                                            "borderRadius": "4px",
                                            "border": "1px solid #CCCCCC"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Select, Checkbox, Radio
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
                                        "content": "Selection Controls",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "select",
                                    "props": {
                                        "options": [
                                            {"label": "Option 1", "value": "1"},
                                            {"label": "Option 2", "value": "2"},
                                            {"label": "Option 3", "value": "3"}
                                        ],
                                        "placeholder": "Select an option",
                                        "style": {
                                            "width": "100%",
                                            "padding": "8px",
                                            "marginBottom": "15px",
                                            "borderRadius": "4px",
                                            "border": "1px solid #CCCCCC"
                                        }
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "checkbox",
                                                "props": {
                                                    "label": "I agree to the terms and conditions",
                                                    "checked": False,
                                                    "style": {
                                                        "marginBottom": "5px"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "checkbox",
                                                "props": {
                                                    "label": "Subscribe to newsletter",
                                                    "checked": True,
                                                    "style": {
                                                        "marginBottom": "5px"
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
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "radio",
                                                "props": {
                                                    "options": [
                                                        {"label": "Option A", "value": "a"},
                                                        {"label": "Option B", "value": "b"},
                                                        {"label": "Option C", "value": "c"}
                                                    ],
                                                    "value": "a"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    # Slider, Switch, DatePicker, TimePicker
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
                                        "content": "Advanced Inputs",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Slider:",
                                                    "style": {"marginBottom": "5px"}
                                                }
                                            },
                                            {
                                                "type": "slider",
                                                "props": {
                                                    "min": 0,
                                                    "max": 100,
                                                    "step": 1,
                                                    "value": 50,
                                                    "style": {
                                                        "width": "100%",
                                                        "marginBottom": "15px"
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
                                            "marginBottom": "15px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "gap": "10px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Switch:",
                                                    "style": {"marginBottom": "0"}
                                                }
                                            },
                                            {
                                                "type": "switch",
                                                "props": {
                                                    "checked": True
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Date Picker:",
                                                    "style": {"marginBottom": "5px"}
                                                }
                                            },
                                            {
                                                "type": "datepicker",
                                                "props": {
                                                    "value": "2025-04-13",
                                                    "style": {
                                                        "width": "100%",
                                                        "padding": "8px",
                                                        "marginBottom": "15px",
                                                        "borderRadius": "4px",
                                                        "border": "1px solid #CCCCCC"
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
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Time Picker:",
                                                    "style": {"marginBottom": "5px"}
                                                }
                                            },
                                            {
                                                "type": "timepicker",
                                                "props": {
                                                    "value": "14:30",
                                                    "style": {
                                                        "width": "100%",
                                                        "padding": "8px",
                                                        "borderRadius": "4px",
                                                        "border": "1px solid #CCCCCC"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    # Rate and Upload
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
                                        "content": "Special Inputs",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Rate:",
                                                    "style": {"marginBottom": "5px"}
                                                }
                                            },
                                            {
                                                "type": "rate",
                                                "props": {
                                                    "value": 3,
                                                    "max": 5
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "p",
                                                "props": {
                                                    "content": "Upload:",
                                                    "style": {"marginBottom": "5px"}
                                                }
                                            },
                                            {
                                                "type": "upload",
                                                "props": {
                                                    "multiple": True,
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