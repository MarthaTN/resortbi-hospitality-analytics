from data_processing.mappers import (
    map_resort,
    map_booking_status,
)


print("RESORT MAPPING")
print(map_resort("ET01"))
print(map_resort("WT01"))
print(map_resort("XYZ"))


print("\nBOOKING STATUS MAPPING")
print(map_booking_status("CN"))
print(map_booking_status("CO"))
print(map_booking_status("XYZ"))