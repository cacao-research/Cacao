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
                    "content": "Welcome to Cacao PWA",
                    "style": {
                        "color": "#f0be9b",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "A deliciously simple PWA using Cacao!",
                    "style": {
                        "color": "#D4A76A"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "Install this as an app on your phone or desktop!",
                    "style": {
                        "color": "#D4A76A"
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    # Simple PWA app - just like the desktop version!
    app.brew(
        type="web",
        title="My Custom PWA",
        host="localhost",
        http_port=1634,
        pwa_config={
            "app_name": "My Custom PWA",
            "app_description": "A simple PWA with custom icons",
            "theme_color": "#f0be9b",
            "background_color": "#FFFFFF",
            "icon_192": "/static/icons/icon-192.png",
            "icon_512": "/static/icons/icon-512.png"
        },
        icon="cacao/core/static/icons/icon-512.png"  # Custom favicon for web (served at /favicon.ico)
    )