from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

keyword_categories = """
    Technical / Product Fields
    - Product number
    - Product name
    - Product code
    - Global order reference
    - ANSI code
    - LIF code
    - Family brand

    Electrical & Photometric Data
    - Nominal wattage
    - Nominal voltage
    - Nominal luminous flux
    - Color temperature
    - Correlated color temperature (CCT)
    - Chromaticity coordinate x
    - Chromaticity coordinate y
    - Color rendering index Ra
    - Illuminated field
    - Light center length (LCL)
    - Useful luminous flux (Φuse)
    - Φuse value refers to luminous flux

    Physical Attributes
    - Lamp base
    - Diameter
    - Length
    - Product weight

    Operating & Lifetime
    - Burning position
    - Nominal lifetime
    - Dimmable

    Environmental & Regulatory
    - Declaration no. in SCIP database
    - Candidate list substance
    - Information according to Art. 33 of EU Regulation (EC) 1907/2006 (REACh)
    - Energy efficiency class
    """

def extract_keywords_from_text(text: str) -> str:
    prompt = f""" 
    You are an intelligent assistant that extracts structured product information from datasheets.
    The following are the required fields:

    {keyword_categories}

    Now, extract all available information from this datasheet in key-value pairs using the field names above.

    Datasheet content:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You extract structured product information from technical datasheets."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
