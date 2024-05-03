import gettext
import polib
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class Translator:
    def __init__(self, localedir, domain, lang_code):
        self.localedir = localedir
        self.domain = domain
        self.lang_code = lang_code
        self.model_name = "facebook/nllb-200-distilled-600M"

        # compile Po
        po_path = f'locales/{self.lang_code}/LC_MESSAGES/{self.domain}.po'
        mo_path = Path(po_path).with_suffix('.mo')
        if Path.exists(Path(po_path)) and not Path.exists(mo_path):
            po = polib.pofile(Path(__file__).parent / po_path)
            # or to save the po file as an mo file
            po.save_as_mofile(Path(__file__).parent / str(mo_path))

        # Load model and tokenizer
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.lang = gettext.translation(self.domain, localedir=self.localedir, languages=[self.lang_code], fallback=True)
        self.lang.install()
        self._ = self.gettext


    def translate_by_llm(self, text, src_lang='eng_Latn'):
        # Use the pipeline to translate text
        translator = pipeline('translation', model=self.model, tokenizer=self.tokenizer,
                              src_lang=src_lang, tgt_lang=self.lang_code, max_length=400)
        output = translator(text)
        translated_text = output[0]['translation_text']
        return translated_text

    def gettext(self, message):
        # Attempt to translate the message using gettext
        translated_message = self.lang.gettext(message)
        # If the translation is the same as the original, assume it's not found and use the custom translation
        if translated_message == message:
            return self.translate_by_llm(message, self.lang_code)
        return translated_message


# Usage example
# translator = Translator('locales', 'app', 'fra_Latn')
# _ = translator._
# # Now use translator.gettext to translate messages
# print(_("Hello, World!"))
# name = "Alice"
# print(_(f"You win! {name}"))
# print(_("You win! {name}").format(name=name))