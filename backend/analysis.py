import subprocess

def generate_business_report(transcribed_text):
    prompt = f"""
Summarize the following transcript into a maximum of 5 short lines.
Only include the most important business insights.
Do NOT exceed 5 lines.
Keep the summary clear and concise.

Transcript:
{transcribed_text}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", prompt],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip() if result.stdout else "No response from LLaMA."

        # HARD LIMIT: Ensure max 5 lines
        lines = output.split("\n")[:5]
        final_output = "\n".join(lines)

        print("🧠 Report Generated")
        return final_output

    except Exception as e:
        return f"Error running LLaMA model: {e}"
