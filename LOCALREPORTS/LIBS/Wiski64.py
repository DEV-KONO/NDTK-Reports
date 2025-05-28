import base64

# Digan Whiskey! 📸, Convierte una foto a Base64!
def Whiskey(route: str):
    with open(route, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")