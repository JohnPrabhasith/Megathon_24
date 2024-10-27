from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def intensity_scorer(text, reference_entry):
    """Score the intensity of the mental health concern"""
    prompt = f"""Rate the intensity of mental health concerns in this text: '{text}'
                Provide a score from 1-10 where:
                1-3: Mild concern
                4-7: Moderate concern
                8-10: Severe concern
                Respond with only the number."""
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a mental health professional who rates the severity of concerns. Respond with only a number from 1 to 10."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )
    
    try:
        intensity = int(response.choices[0].message.content.strip())
        return min(max(intensity, 1), 10)
    except:
        return reference_entry['Intensity']