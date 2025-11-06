import subprocess

def generate_business_report(transcribed_text):
    prompt = f"""
    Analyze the following business pitch and provide:
    1. Summary
    2. Market Viability
    3. Key Insights
    4. Improvements Needed
    Text: {transcribed_text}
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", prompt],
            capture_output=True,
            text=True
        )
        print("🧠 Report Generated")
        return result.stdout.strip() if result.stdout else "No response from LLaMA."
    except Exception as e:
        return f"Error running LLaMA model: {e}"
