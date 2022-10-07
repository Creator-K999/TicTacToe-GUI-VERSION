from json import loads

with open("../../windows/startup_font_settings.json") as file:
    font_settings = loads(file.read())
