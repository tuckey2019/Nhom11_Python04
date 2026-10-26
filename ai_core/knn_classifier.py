"""
Module Phân loại Phương tiện Bằng Máy Học (K-Nearest Neighbors Classifier).
Chịu trách nhiệm:
- Huấn luyện mô hình phân loại không tham số KNN (K-Nearest Neighbors).
- Nhận diện phân loại xe (MiniCar, StandardCar, LargeCar) dựa trên kích thước: Chiều dài và Chiều rộng.
- Áp dụng khoảng cách Euclidean và cơ chế biểu quyết đa số (Majority Voting).
"""

import math
from typing import List, Tuple
from utils.json_handler import JSONHandler
from config import FILE_CAR_DATA


class KNNClassifier:
    """
    Lớp phân loại kích thước xe tự động hỗ trợ hệ thống xếp chỗ thông minh.
    """
    def __init__(self, k: int = 3):
        self.k = k
        self.dataset = JSONHandler.read_json(FILE_CAR_DATA)

    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Tính khoảng cách Euclidean giữa 2 điểm vector đặc trưng (chiều dài, chiều rộng)"""
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def predict(self, length: float, width: float) -> str:
        """
        Dự đoán phân loại xe mới vào bãi:
        1. Tính khoảng cách từ kích thước xe đến toàn bộ mẫu trong tập huấn luyện
        2. Sắp xếp khoảng cách tăng dần
        3. Chọn K mẫu gần nhất
        4. Biểu quyết nhãn xuất hiện nhiều nhất (Majority Vote)
        """
        if not self.dataset:
            return "StandardCar"  # Cơ chế dự phòng an toàn nếu thiếu tập dữ liệu

        distances = []
        new_car_point = (length, width)

        # 1. Tính khoảng cách
        for car in self.dataset:
            known_point = (car["length"], car["width"])
            dist = self._calculate_distance(new_car_point, known_point)
            distances.append((dist, car["label"]))

        # 2. Sắp xếp khoảng cách từ gần đến xa
        distances.sort(key=lambda x: x[0])

        # 3. Lấy K hàng xóm gần nhất
        k_nearest = distances[:self.k]

        # 4. Biểu quyết lấy nhãn chiếm ưu thế
        labels = [item[1] for item in k_nearest]
        predicted_label = max(set(labels), key=labels.count)

        return predicted_label
