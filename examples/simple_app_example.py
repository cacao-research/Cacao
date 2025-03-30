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
                    "content": "A deliciously simple web framework!",
                    "style": {
                        "color": "#D4A76A"
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew(http_port=1644, ws_port=1643)  # Run the app like brewing hot chocolate!
