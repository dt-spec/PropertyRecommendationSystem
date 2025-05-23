import json
from src.recommender import recommend_top_3
from src.evaluator import precision_at_3
from src.explainability import explain_why_selected

# Load validation set
with open("data/val_processed.json") as f:
    val_data = json.load(f)

scores = []
for appraisal in val_data:
    try:
        subject = appraisal.get("subject", {})
        candidates = appraisal.get("properties", [])
        comps = appraisal.get("comps", [])

        if not subject or not candidates or not comps:
            continue

        # Build a map from address to id for candidates
        address_to_id = {c["address"].strip().lower(): c["id"] for c in candidates if "address" in c and "id" in c}
        # Get the ids of the comps by matching address
        true_comps = []
        for comp in comps:
            comp_address = comp.get("address", "").strip().lower()
            if comp_address in address_to_id:
                true_comps.append(address_to_id[comp_address])

        if not true_comps:
            continue

        predicted = recommend_top_3(subject, candidates)
        score = precision_at_3(predicted, true_comps)
        scores.append(score)

        print(f"\nSubject: {subject.get('address', 'N/A')}")
        print("Top 3 Recommended Comps:")
        for idx, comp_id in enumerate(predicted, 1):
            comp = next((c for c in candidates if c["id"] == comp_id), None)
            if comp:
                explanations = explain_why_selected(subject, comp)
                print(f"  {idx}. {comp.get('address', 'N/A')} (ID: {comp_id})")
                print(f"     Reason: {', '.join(explanations) if explanations else 'Most similar overall'}")
    except Exception as e:
        print(f"Error processing appraisal: {e}")
        continue

if scores:
    print("\nAverage Precision@3:", sum(scores) / len(scores))
else:
    print("No valid appraisals were processed.")
