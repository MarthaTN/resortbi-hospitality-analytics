from data_processing.transformers import (
    transform_name,
    transform_country,
    transform_date,
    transform_amount,
)


print("NAME")
print(transform_name("  maria   garcia "))


print("\nCOUNTRY")
print(transform_country("  nAmIbIa "))


print("\nDATE")
print(transform_date("13/09/26"))


print("\nAMOUNT")
print(transform_amount("NAD 4,800"))