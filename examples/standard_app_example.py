"""Standard Cacao application example demonstrating core features."""

import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Welcome to Cacao {%icon-fa-home%}",
                    "style": {
                        "color": "#6B4226",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "This is a standard app example showing features like icons: {%icon-fa-star color=#FFD700%}"
                }
            },
            {
                "type": "div",
                "props": {
                    "style": {
                        "marginTop": "20px",
                        "padding": "15px",
                        "backgroundColor": "#f5f5f5",
                        "borderRadius": "4px"
                    }
                },
                "children": [
                    {
                        "type": "h3",
                        "props": {
                            "content": "Demo Features {%icon-fa-list-ul%}"
                        }
                    },
                    {
                        "type": "ul",
                        "props": {
                            "children": [
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "{%icon-fa-check color=#4CAF50%} Routing"
                                    }
                                },
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "{%icon-fa-check color=#4CAF50%} Component System"
                                    }
                                },
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "{%icon-fa-check color=#4CAF50%} Icon Support"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    app.brew()