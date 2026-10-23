
from models.vehicle import Vehicle

class ParkingSlot:
    def __init__(self, slot_id: str, slot_type: str = "standard"):
        self.slot_id = slot_id              # VD: "A01", "B05"
        self.slot_type = slot_type          # "compact", "standard", "vip", "large"
        self.is_occupied = False            # Trạng thái (Trống / Đang đỗ)
        self.current_vehicle = None         # Chứa đối tượng Vehicle nếu có xe

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """Thực hiện đỗ xe vào vị trí"""
        if self.is_occupied:
            return False # Chỗ đã có xe
        self.current_vehicle = vehicle
        self.is_occupied = True
        return True

    def remove_vehicle(self) -> Vehicle:
        """Lấy xe ra khỏi vị trí và trả về chiếc xe đó để tính tiền"""
        if not self.is_occupied:
            return None
        vehicle = self.current_vehicle
        self.current_vehicle = None
        self.is_occupied = False
        return vehicle
        
    def to_dict(self) -> dict:
        """Chuyển đổi thành Dictionary để lưu vào JSON"""
        data = {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type,
            "is_occupied": self.is_occupied
        }
        if self.current_vehicle:
            data["vehicle_info"] = self.current_vehicle.get_info()
        return data