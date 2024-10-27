from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def polarity_finder(text, reference_entry):
    """Determine polarity based on reference data and LLM"""
    prompt = f"Analyze this text: '{text}'. Determine if it expresses a positive, negative, or neutral sentiment. Answer with only one word: positive, negative, or neutral."
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a mental health professional who analyzes sentiment. Respond with exactly one word: positive, negative, or neutral."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )
    
    llm_polarity = response.choices[0].message.content.strip().lower()
    return llm_polarity if llm_polarity != reference_entry['Polarity'].lower() else reference_entry['Polarity'].lower()