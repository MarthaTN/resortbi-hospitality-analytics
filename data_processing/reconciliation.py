def reconcile_amounts(source_a, source_b):
    if source_a == source_b:
        return {
            "status": "MATCH",
            "difference": 0,
        }

    difference = source_a - source_b

    return {
        "status": "MISMATCH",
        "difference": difference,
    }