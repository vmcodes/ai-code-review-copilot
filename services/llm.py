"""
Safe LLM module (won't crash if transformers/torch fails)
"""

def llm_review(code: str) -> str:
    try:
        from transformers import pipeline

        pipe = pipeline("text-generation", model="distilgpt2")

        prompt = f"Review this code:\n{code[:500]}"
        result = pipe(prompt, max_length=150)

        return result[0]["generated_text"]

    except Exception as e:
        return f"[LLM Skipped: {str(e)}]"