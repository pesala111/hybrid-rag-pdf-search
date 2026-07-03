import re
from typing import Dict

regex_field_patterns = {
        "Product number": r"Product number.*?(\d{5,})",
        "Product name": r"Product name.*?:?\s*([^\n]+)",
        "Product code": r"Product code.*?(\d{5,})",
        "Global order reference": r"Global order reference.*?:?\s*([^\n]+)",
        "ANSI code": r"ANSI code.*?:?\s*([^\n]+)",
        "LIF code": r"LIF code.*?:?\s*([^\n]+)",
        "Family brand": r"Family brand.*?:?\s*([^\n]+)",
        "Nominal wattage": r"Nominal wattage.*?([\d.]+\s*W)",
        "Nominal voltage": r"Nominal voltage.*?([\d.]+\s*V)",
        "Nominal luminous flux": r"Nominal luminous flux.*?([\d.]+\s*lm)",
        "Color temperature": r"Color temperature.*?([\d.]+\s*K)",
        "Correlated color temperature (CCT)": r"Correlated color temperature.*?([\d.]+\s*K)",
        "Chromaticity coordinate x": r"Chromaticity coordinate x.*?([\d.]+)",
        "Chromaticity coordinate y": r"Chromaticity coordinate y.*?([\d.]+)",
        "Color rendering index Ra": r"Color rendering index Ra.*?([\d.]+)",
        "Illuminated field": r"Illuminated field.*?([^\n]+)",
        "Light center length (LCL)": r"Light center length.*?([\d.]+\s*mm)",
        "Useful luminous flux": r"Useful luminous flux.*?([^\n]+)",
        "Lamp base": r"Lamp base.*?([^\n]+)",
        "Diameter": r"Diameter.*?([\d.]+\s*mm)",
        "Length": r"Length.*?([\d.]+\s*mm)",
        "Product weight": r"Product weight.*?([\d.]+\s*g)",
        "Burning position": r"Burning position.*?([^\n]+)",
        "Nominal lifetime": r"Nominal lifetime.*?([\d.]+\s*h[r]?\b)",
        "Dimmable": r"\bDimmable\b",
        "Energy efficiency class": r"Energy efficiency class.*?([^\n]+)",
        "Category": r"Category.*?:?\s*([^\n]+)",
        "Nominal current": r"Nominal current.*?([\d.]+\s*A)",
        "Type of current": r"Type of current.*?:?\s*([^\n]+)",
        "Working distance": r"Working distance.*?([\d.]+\s*mm)",
        "Electrode gap": r"Electrode gap.*?([\d.]+\s*mm)",
        "Primary article identifier": r"Primary article identifier.*?:?\s*([^\n]+)",
        "Lamp type": r"Lamp type.*?:?\s*([^\n]+)",
        "Luminous efficacy": r"Luminous efficacy.*?([\d.]+\s*lm/W)",
        "Ignition voltage": r"Ignition voltage.*?([\d.]+\s*V)",
}


def extract_keywords_with_regex(text: str) -> Dict[str, str]:
        """Extract structured product fields from PDF text using regex patterns.

            Returns a dict mapping field names to extracted values.
                Fields whose label appears in the text but whose value could not be
                    parsed are silently skipped to keep the output clean.
                        """
        extracted: Dict[str, str] = {}

    for field, pattern in regex_field_patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                                value = match.group(1).strip() if match.lastindex else match.group(0).strip()
                                extracted[field] = value

            return extracted
