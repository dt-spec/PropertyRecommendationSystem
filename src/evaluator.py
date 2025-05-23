def precision_at_3(predicted_ids, actual_ids):
    correct = set(predicted_ids) & set(actual_ids)
    return len(correct) / 3
