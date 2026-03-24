from googletrans import Translator

translator = Translator()

def translate_report(report_text, target_language):
    try:
        result = translator.translate(report_text, dest=target_language)
        print(f"🌍 Translated report ready in {target_language}.")
        return result.text
    except Exception as e:
        return f"Translation failed: {e}"