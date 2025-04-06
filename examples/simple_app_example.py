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
                    "content": "Welcome to Cacao 1",
                    "style": {
                        "color": "#6B4226",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "A deliciously simple web framework!",
                    "style": {
                        "color": "#6B4226"
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew()  # Run the app like brewing hot chocolate!
