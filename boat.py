import uuid

class Boat:
    def __init__(self, brand_name, name, year, length):
        self.id = str(uuid.uuid4())  # Generate a unique ID
        self.brand_name = brand_name
        self.name = name
        self.year = year
        self.length = length
        self.schedule = []  # Initialize an empty list for schedule

    def add_schedule(self, from_date, to_date, price):
        self.schedule.append({
            "from_date": from_date,
            "to_date": to_date,
            "price": price
        })

    def __str__(self):
        return f"Boat ID: {self.id}\nBrand: {self.brand_name}\nName: {self.name}\nYear: {self.year}\nLength: {self.length}\nSchedule: {self.schedule}"

# Example usage:
boat1 = Boat("Dufour", "Sailing Yacht 35", 2020, 35)
boat1.add_schedule("2023-10-20", "2023-10-27", 1500)
boat1.add_schedule("2023-11-03", "2023-11-10", 1200)

print(boat1)
