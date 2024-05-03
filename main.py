import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from random import random
from translator import Translator

from pathlib import Path
app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/{lang}/", response_class=HTMLResponse)
def form(request: Request, lang: str = "en"):
    translator = Translator('locales', 'app', lang)
    _ = translator._
    return templates.TemplateResponse("index.html", {"request": request, "_": _, "lang": lang})

@app.post("/{lang}/", response_class=HTMLResponse)
def form_post(request: Request, name: str = Form(...), text: str = Form(...), lang: str = "en"):
    translator = Translator('locales', 'app', lang)
    _ = translator._
    win_chance = random()
    if win_chance < 0.9:
        message = _("You win! {name}").format(name=name)
    else:
        message = _("You lose! {name}").format(name=name)
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "name": name, "text1": _(text), "_": _, "lang": lang})

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
