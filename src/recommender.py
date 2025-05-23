from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import re

def clean_numeric(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        val = val.lower().replace(",", "").replace("sqft", "").replace("sq ft", "").replace("sq. ft", "").strip()
        if val in ["", "n/a", "na", "none", "null"]:
            return 0.0
        # Extract numeric part
        match = re.search(r"[\d.]+", val)
        if match:
            return float(match.group(0))
        return 0.0
    return 0.0

def get_features(property):
    gla = clean_numeric(property.get("gla"))
    lot_size = clean_numeric(property.get("lot_size_sf"))
    bedrooms = clean_numeric(property.get("bedrooms"))
    full_baths = clean_numeric(property.get("full_baths"))
    half_baths = clean_numeric(property.get("half_baths"))
    bathrooms = full_baths + 0.5 * half_baths
    year_built = clean_numeric(property.get("year_built"))
    return np.array([
        gla,
        lot_size,
        bedrooms,
        bathrooms,
        year_built
    ])

def recommend_top_3(subject, candidates):
    subject_vector = get_features(subject).reshape(1, -1)
    candidate_vectors = np.array([get_features(c) for c in candidates])
    distances = euclidean_distances(subject_vector, candidate_vectors)[0]
    
    # Get top 3 indices
    top_indices = distances.argsort()[:3]
    return [candidates[i]["id"] for i in top_indices]
