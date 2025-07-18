import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px",
                "fontFamily": "Arial, sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Welcome to Cacao",
                    "style": {
                        "color": "#f0be9b",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "A deliciously simple desktop app using Cacao!",
                    "style": {
                        "color": "#D4A76A"
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    # Simple desktop app - just like before!
    app.brew(
        type="desktop",
        title="Cacao",
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
        icon="cacao/core/static/icons/icon-512.png"  # Custom favicon for web (served at /favicon.ico)
    )