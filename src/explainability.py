import re
from datetime import datetime

def clean_numeric(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        val = val.lower().replace(",", "").replace("sqft", "").replace("sq ft", "").replace("sq. ft", "").strip()
        if val in ["", "n/a", "na", "none", "null"]:
            return 0.0
        match = re.search(r"[\d.]+", val)
        if match:
            return float(match.group(0))
        return 0.0
    return 0.0

def explain_why_selected(subject, comp):
    explanations = []
    # GLA
    gla_sub = clean_numeric(subject.get("gla"))
    gla_comp = clean_numeric(comp.get("gla"))
    if abs(gla_sub - gla_comp) < 100:
        explanations.append("similar GLA")
    # Lot size
    lot_sub = clean_numeric(subject.get("lot_size_sf"))
    lot_comp = clean_numeric(comp.get("lot_size_sf"))
    if abs(lot_sub - lot_comp) < 200:
        explanations.append("close lot size")
    # Bedrooms
    if clean_numeric(subject.get("bedrooms")) == clean_numeric(comp.get("bedrooms")):
        explanations.append("same number of bedrooms")
    # Bathrooms
    def get_bathrooms(p):
        return clean_numeric(p.get("full_baths")) + 0.5 * clean_numeric(p.get("half_baths"))
    if abs(get_bathrooms(subject) - get_bathrooms(comp)) < 1:
        explanations.append("similar number of bathrooms")
    # Year built
    year_sub = clean_numeric(subject.get("year_built"))
    year_comp = clean_numeric(comp.get("year_built"))
    if year_sub and year_comp and abs(year_sub - year_comp) <= 5:
        explanations.append("similar year built")
    # Sale date (if available)
    date_sub = subject.get("close_date")
    date_comp = comp.get("close_date")
    try:
        if date_sub and date_comp:
            d1 = datetime.strptime(date_sub[:10], "%Y-%m-%d")
            d2 = datetime.strptime(date_comp[:10], "%Y-%m-%d")
            if abs((d1 - d2).days) < 180:
                explanations.append("recent sale date")
    except Exception:
        pass
    return explanations
