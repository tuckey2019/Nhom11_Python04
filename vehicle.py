import random
from datetime import datetime

class Vehicle:
    def __init__(self, license_plate: str, owner_name: str = "Khách vãng lai"):
        self.license_plate = license_plate
        self.owner_name = owner_name
        self.entry_time = datetime.now()
        # NÂNG CAO: Tự động sinh mã vé ngẫu nhiên khi khởi tạo xe
        self.ticket_code = f"TK-{random.randint(10000, 99999)}"
        
    def calculate_fee(self, hours_parked: float, slot_type: str) -> float:
        pass

    def get_info(self) -> dict:
        return {
            "ticket_code": self.ticket_code,
            "license_plate": self.license_plate,
            "owner_name": self.owner_name,
            "entry_time": self.entry_time.strftime('%Y-%m-%d %H:%M:%S'),
            "vehicle_type": self.__class__.__name__
        }

class MiniCar(Vehicle):
    BASE_RATE = 15000
    def calculate_fee(self, hours_parked: float, slot_type: str) -> float:
        total = self.BASE_RATE * max(1, hours_parked)
        if slot_type == "compact": return total * 0.8
        return total

class StandardCar(Vehicle):
    BASE_RATE = 20000
    def calculate_fee(self, hours_parked: float, slot_type: str) -> float:
        return self.BASE_RATE * max(1, hours_parked)

class LargeCar(Vehicle):
    BASE_RATE = 30000
    def calculate_fee(self, hours_parked: float, slot_type: str) -> float:
        total = self.BASE_RATE * max(1, hours_parked)
        if slot_type == "vip": return total * 1.2
        return total
        
class Motorbike(Vehicle):
    BASE_RATE = 5000
    def calculate_fee(self, hours_parked: float, slot_type: str) -> float:
        return self.BASE_RATE * max(1, hours_parked)