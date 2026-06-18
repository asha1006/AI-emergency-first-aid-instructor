import streamlit as st
from google import genai
from PIL import Image


def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )


SYSTEM_PROMPT = """
You are an AI Emergency First Aid Assistant.

Rules:
1. Give only safe first-aid guidance.
2. Do not claim a final medical diagnosis.
3. Always include severity: Low, Medium, High, or Critical.
4. Always include step-by-step instructions.
5. Mention whether hospital/ambulance is required.
6. Use simple language.
7. Add: This is first-aid guidance only. Contact medical professionals immediately in serious cases.
"""


def analyze_text_emergency(user_text):
    try:

        client = get_client()

        prompt = f"""
{SYSTEM_PROMPT}

Emergency Situation:
{user_text}

Give the response in the following format:

🚨 Severity:
Possible Condition:

🩹 Immediate First Aid Steps:
1.
2.
3.
4.

🏥 Hospital Advice:

⚠️ Safety Note:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_msg = str(e)

        if "503" in error_msg:
            return """
🚨 AI Service Temporarily Busy

Google Gemini is currently experiencing high demand.

Please:
1. Wait a few minutes.
2. Try again.
3. Contact emergency services immediately if the situation is serious.

⚠️ This is only a temporary server issue.
"""

        return f"Error: {error_msg}"


def analyze_image_emergency(image_file):
    try:

        client = get_client()

        image = Image.open(image_file)

        # Reduce image size for faster processing
        image.thumbnail((1024, 1024))

        prompt = f"""
{SYSTEM_PROMPT}

Analyze this emergency or injury image carefully.

IMPORTANT:
- Do not provide a final medical diagnosis.
- Describe the possible injury.
- Estimate severity.
- Give immediate first-aid instructions.
- Advise whether hospital treatment is needed.

Response Format:

🚨 Severity:
Possible Condition:

🩹 Immediate First Aid Steps:
1.
2.
3.
4.

🏥 Hospital Advice:

⚠️ Safety Note:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )

        return response.text

    except Exception as e:

        error_msg = str(e)

        if "503" in error_msg:
            return """
🚨 AI Service Temporarily Busy

Google Gemini is currently experiencing high demand.

Please:
1. Wait a few minutes.
2. Try again.
3. Contact emergency services immediately if the situation is serious.

⚠️ This is only a temporary server issue.
"""

        return f"Error: {error_msg}"