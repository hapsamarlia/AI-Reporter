import subprocess

def chatbot_response(question, context):
    prompt = f"""
You are a business pitch assistant.

Context:
{context}

Question:
{question}

Answer in a maximum of 3 short lines.
Keep the response clear, professional, and relevant to the business pitch.
Do NOT give long explanations.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", prompt],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip() if result.stdout else "No chatbot response from LLaMA."

        # HARD LIMIT: max 3 lines
        lines = output.split("\n")[:3]
        final_output = "\n".join(lines)

        return final_output

    except Exception as e:
        return f"Error: {e}"
