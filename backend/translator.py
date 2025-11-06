from googletrans import Translator

def translate_report(report_text, target_language="fr"):
    try:
        translator = Translator()
        result = translator.translate(report_text, dest=target_language)
        print("🌍 Translated report ready.")
        return result.text
    except Exception as e:
        return f"Translation failed: {e}"
