# Web App Globalization and Localization with FastAPI

## Introduction
Globalization and localization are essential for making web application accessible and usable by users from different regions and language backgrounds. This guide will walk you through the process of implementing globalization and localization in a FastAPI web application.

## 1. Using Client Side Translator
To enable translation in the browser, you can utilize browser extensions or built-in features. Here are translation options for popular browsers:
- **Chrome**: [Google Translate](https://support.google.com/chrome/answer/173424?hl=en&co=GENIE.Platform%3DDesktop)
- **Firefox**: [Multi-language Translator](https://www.mozilla.org/en-US/firefox/features/translate/)
- **Edge**: [Microsoft Translator](https://support.microsoft.com/en-us/topic/use-microsoft-translator-in-microsoft-edge-browser-4ad1c6cb-01a4-4227-be9d-a81e127fcb0b)
<br> 

Using these translator is easy and no code change is needed but the results may depend on the browser chosen, which results in inconsistency. 

- Accept-Language Header: 

When a user navigates to a website, their browser sends an HTTP request to the web server.
This request includes an **Accept-Language** header, which indicates the user's preferred languages based on their browser settings.
The Accept-Language header contains a list of language codes (e.g., en-US, fr-FR) in order of preference, separated by commas.
The webserver can use this to serve different contents, for example:

```
app = FastAPI()

# Initialize Jinja2Templates instance
templates = Jinja2Templates(directory="templates")

# Example content in different languages
content = {
    "en": "Hello, world!",
    "fr": "Bonjour tout le monde!",
    "es": "¡Hola, mundo!"
}

@app.get("/")
async def read_root(request: Request):
    # Get the Accept-Language header from the request
    accept_language = request.headers.get("Accept-Language")
    
    # Parse the Accept-Language header to get the preferred language(s)
    preferred_languages = accept_language.split(",") if accept_language else []
    
    # Extract the language code from each preferred language
    languages = [Locale.parse(lang.strip().split(";")[0]) for lang in preferred_languages]
    
    # Find the best match language for content
    matched_language = "en"  # Default to English
    for lang in languages:
        if str(lang) in content:
            matched_language = str(lang)
            break
    
    # Serve content based on the matched language
    return templates.TemplateResponse("index.html", {"request": request, "content": content[matched_language]})
```

## 2. Translation: GETTEXT, PO and MO Files 
### Concept

- **Gettext**
GNU gettext is a set of tools and libraries designed to facilitate internationalization (i18n) 
and localization (l10n) of software applications. It provides a framework for creating and managing translations of text strings.
- **PO Files (Portable Object)**: These are human-readable files containing pairs of original strings and their translated versions.
- **MO Files (Machine Object)**: These are compiled versions of PO files that are optimized for machine use.

The process often contain these steps:
1. **String Extraction**: scan source code files to extract translatable strings marked with specific markers, typically function calls or macros. These strings are then collected into a template file, often referred to as a "POT" (Portable Object Template) file.
2. **Translation Management**: translators manage translations manually through Portable Object (PO) files. 
These PO files contain pairs of original strings and their translated terms. Translators can use automated tools to manipulate files as well.
3. **Compilation**: Once translations are available, PO files are compiled into Machine Object (MO) files. MO files are binary files optimized for efficient storage and retrieval of translations. These files are machine dependent. 
During runtime, applications can load the appropriate MO file based on the user's language preferences and use the translated strings as needed.

## 3. Babel
[Babel](https://babel.pocoo.org/en/latest/) includes a command-line interface for working with message catalogs, 
similar to the various GNU gettext tools commonly available on Linux/Unix systems. 
[PyBabel](https://pypi.org/project/pybabel/) is a Python library that integrates with popular web frameworks like Flask and Django. Here's a simple example of using PyBabel with a FastAPI application:

You can install PyBabel via pip:
```bash
pip install pybabel
```
###Example:
Suppose we have a FastAPI application with the following directory structure:
```
project/
├── app/
│   ├── main.py
│   └── templates/
│       └── index.html
```
Use "_" in your index.html for the text that needs translation (jinja2 templates)
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Website{% endblock %}</title>
</head>
<body>
    <h1>{% block heading %}{{ _("Welcome") }}{% endblock %}</h1>
    <p>{{ _("This is a sample page") }}</p>
</body>
</html>
```
Define a pybabel config with the extraction rules, such as 
```
[python: **.py]
[jinja2: **/templates/**.html]
```
After install pybabl, you can run
`pybabel extract -F babel.cfg -o messages.pot .
`

You should now get a template of your translation
```
#: templates/index.html:7
msgid "Welcome"
msgstr ""

#: templates/index.html:8
msgid "This is a sample page"
msgstr ""
```
Now run this command `pybabel init -i messages.pot -d locales -l fr`
this will initialize a structure under *locales* folder with a copy of the POT template, translators can now work on the translation and
once it is done, you can use this command  `pybabel compile -d locales` to compile it to MO files
<br><br>
below code shows an integration of translation with FastAPI
```
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import gettext

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Translation setup using gettext or pybabel that implements it
def get_translation(lang):
    try:
        return gettext.translation('app', localedir='locales', languages=[lang])
    except FileNotFoundError:
        return gettext.NullTranslations()

@app.get("/{lang}/", response_class=HTMLResponse)
def form(request: Request, lang: str = "en"):
    _ = get_translation(lang).gettext
    return templates.TemplateResponse("index.html", {"request": request, "_": _, "lang": lang})
```
User will get the custom translation based on their request, for example http://127.0.0.1/fr/ will display french translation 

### Translation Tools
Various tools can be used for translating PO files, including:
- **Poedit**: A popular cross-platform gettext [translation editor](https://poedit.net/).
- **Pofile.Net**:Free [online editor](https://pofile.net/free-po-editor)
- **No Language Left Behind (NLLB)** AI breakthrough project that open-sources models capable of delivering evaluated, high-quality translations directly between 200 languages
Recent advancements in natural language processing have led to the development of powerful Neural Language Models (NLMs).
See [translate.py](./translate.py) as an example for generating translations.
