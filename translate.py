# Load model directly
import polib
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

src = 'eng_Latn'
target_lang = 'fra_Latn'


def translate_po_file(input_po_path, output_po_path, src_lang="eng_Latn", dest_lang="fra_Latn"):
    # Load the input .po file
    po = polib.pofile(input_po_path)

    # Process each entry in the .po file
    for entry in po:
        src_text = entry.msgid
        translator = pipeline('translation', 
            model=model, 
            tokenizer=tokenizer, 
            src_lang=src_lang,
            tgt_lang=target_lang, 
            max_length = 400)
        output = translator(src_text)
        translated_text = output[0]['translation_text']    
        entry.msgstr = translated_text
    # Save the translated .po file
    with open(output_po_path, 'w', encoding='utf-8') as f:
        po.save(output_po_path)


if __name__ == "__main__":
    translate_po_file('template.po', 'app.po')