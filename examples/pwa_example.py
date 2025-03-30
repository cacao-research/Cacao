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
    # Run as a desktop application using the unified brew method
    app.brew(
        type="desktop",
        title="Cacao",
        width=800,
        height=600,
        resizable=True,
        fullscreen=False
    )
