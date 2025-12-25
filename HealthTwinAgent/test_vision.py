import os
import json
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_meal(image_path="meal.jpg"):
    print(f"📸 Analyzing {image_path}...")
    base64_image = encode_image(image_path)

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": "Analyze this meal. Return ONLY a JSON object with these exact keys: "
                            "{'calories': int, 'protein': int, 'carbs': int, 'fat': int, "
                            "'fiber': int, 'sugar': int, 'description': str}"
                },
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }],
        model="llama-3.2-11b-vision-preview", 
    )

    # Parse the response
    new_meal = json.loads(chat_completion.choices[0].message.content)
    
    # UPDATE STATE.JSON (Data Transformation Step)
    with open('state.json', 'r+') as f:
        data = json.load(f)
        
        # Increment all nutrient totals
        for nutrient in ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar']:
            data['current_day'][nutrient] += new_meal.get(nutrient, 0)
        
        data['current_day']['last_meal'] = new_meal['description']
        
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
    print(f"✅ State Updated: {new_meal['description']}")
    

if __name__ == "__main__":
    analyze_meal()