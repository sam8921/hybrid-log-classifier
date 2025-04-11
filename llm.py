import os
from dotenv import load_dotenv
from groq import Groq
import re

# 1. Load environment variables FIRST
load_dotenv()

# 2. Get API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# 3. Initialize Groq client (SIMPLIFIED version)
groq = Groq(api_key=api_key)

def classify_with_llm(log_msg):
    """
    Classify log messages using Groq's LLM
    Returns one of: "Workflow Error", "Deprecation Warning", or "Unclassified"
    """
    prompt = f'''Classify the log message into one of these categories: 
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category> </category> tags. 
    Log message: {log_msg}'''

    try:
        response = groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",  # Recommended model
            temperature=0.5
        )
        
        content = response.choices[0].message.content
        match = re.search(r'<category>(.*?)<\/category>', content, flags=re.DOTALL)
        return match.group(1).strip() if match else "Unclassified"
    
    except Exception as e:
        print(f"Classification failed: {str(e)}")
        return "LLM Error"

if __name__ == "__main__":
    # Test cases
    tests = [
        "Case escalation for ticket ID 7324 failed because...",
        "The 'ReportGenerator' module will be retired...",
        "System reboot initiated by user 12345."
    ]
    
    for test in tests:
        print(f"Test: {test[:50]}...")
        print("Result:", classify_with_llm(test))
        print("-" * 50)