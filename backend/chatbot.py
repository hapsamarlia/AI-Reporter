import subprocess

def chatbot_response(question, context):
    prompt = f"""
    Context: {context}
    Question: {question}
    Provide a short, clear answer related to the business pitch.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.stdout else "No chatbot response from LLaMA."
    except Exception as e:
        return f"Error: {e}"
