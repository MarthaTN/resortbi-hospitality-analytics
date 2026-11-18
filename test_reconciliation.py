from data_processing.reconciliation import reconcile_amounts


print("MATCH")
print(reconcile_amounts(3500, 3500))


print("\nMISMATCH")
print(reconcile_amounts(3500, 3200))