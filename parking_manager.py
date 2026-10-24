# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:55:53 2026

@author: DELL
"""


import re
import csv
import os
from datetime import datetime


class ParkingManager:
    """Quản lý nghiệp vụ bãi đỗ xe Smart Parking."""

    # Đơn giá gửi xe theo giờ
    RATES = {
        "Motorbike": 5000,
        "MiniCar": 15000,
        "StandardCar": 15000,
        "LargeCar": 30000
    }

    def __init__(self, total_slots=60):
        self.total_slots = total_slots
        self.vehicles = {}
        self.tickets = {}
        self.monthly_passes = set()
        self.next_ticket_number = 1

    # 1. Kiểm tra định dạng biển số xe
    def validate_license_plate(self, license_plate):
        pattern = r"^\d{2}[A-Z]{1,2}-\d{3}\.\d{2}$"
        return bool(re.fullmatch(pattern, license_plate.upper()))

    # 2. Kiểm tra số chỗ còn trống
    def get_available_slots(self):
        return self.total_slots - len(self.vehicles)

    # 3. Đăng ký vé tháng
    def register_monthly_pass(self, license_plate):
        license_plate = license_plate.upper().strip()

        if not self.validate_license_plate(license_plate):
            raise ValueError("Biển số xe không đúng định dạng.")

        self.monthly_passes.add(license_plate)

    # 4. Tiếp nhận xe vào bãi
    def check_in(self, license_plate, vehicle_type):
        license_plate = license_plate.upper().strip()

        if not self.validate_license_plate(license_plate):
            raise ValueError("Biển số xe không đúng định dạng.")

        if vehicle_type not in self.RATES:
            raise ValueError("Loại xe không hợp lệ.")

        if license_plate in self.vehicles:
            raise ValueError("Xe này đang ở trong bãi.")

        if self.get_available_slots() <= 0:
            raise ValueError("Bãi xe đã hết chỗ.")

        ticket_id = f"TK-{self.next_ticket_number:05d}"
        self.next_ticket_number += 1

        ticket = {
            "ticket_id": ticket_id,
            "license_plate": license_plate,
            "vehicle_type": vehicle_type,
            "entry_time": datetime.now(),
            "exit_time": None,
            "fee": 0,
            "monthly_pass": license_plate in self.monthly_passes
        }

        self.vehicles[license_plate] = ticket
        self.tickets[ticket_id] = ticket

        return ticket.copy()

    # 5. Tính phí gửi xe
    def calculate_fee(self, entry_time, exit_time, vehicle_type,
                      monthly_pass=False):
        if monthly_pass:
            return 0

        if vehicle_type not in self.RATES:
            raise ValueError("Loại xe không hợp lệ.")

        seconds = (exit_time - entry_time).total_seconds()

        if seconds < 0:
            raise ValueError("Thời gian ra bãi không hợp lệ.")

        # Tính mỗi giờ, có phát sinh thời gian thì tính thêm 1 giờ
        hours = max(1, int((seconds + 3599) // 3600))

        return hours * self.RATES[vehicle_type]

    # 6. Xử lý xe ra khỏi bãi
    def check_out(self, license_plate):
        license_plate = license_plate.upper().strip()

        if license_plate not in self.vehicles:
            raise ValueError("Không tìm thấy xe trong bãi.")

        ticket = self.vehicles[license_plate]
        exit_time = datetime.now()

        fee = self.calculate_fee(
            ticket["entry_time"],
            exit_time,
            ticket["vehicle_type"],
            ticket["monthly_pass"]
        )

        ticket["exit_time"] = exit_time
        ticket["fee"] = fee

        result = ticket.copy()
        result["duration_hours"] = max(
            1,
            int(((exit_time - ticket["entry_time"]).total_seconds()
                 + 3599) // 3600)
        )

        del self.vehicles[license_plate]

        return result

    # 7. Lấy danh sách xe đang ở trong bãi
    def get_parked_vehicles(self):
        return [ticket.copy() for ticket in self.vehicles.values()]

    # 8. Tính tổng doanh thu trong ngày
    def get_daily_revenue(self, date=None):
        if date is None:
            date = datetime.now().date()

        total = 0

        for ticket in self.tickets.values():
            exit_time = ticket["exit_time"]

            if exit_time is not None and exit_time.date() == date:
                total += ticket["fee"]

        return total

    # 9. Xuất báo cáo CSV
    def export_csv(self, filename="parking_report.csv"):
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Ma ve", "Bien so", "Loai xe",
                "Thoi gian vao", "Thoi gian ra",
                "Phi gui xe", "Trang thai"
            ])

            for ticket in self.tickets.values():
                status = (
                    "Đang gửi - chưa thanh toán"
                    if ticket["exit_time"] is None
                    else "Đã ra bãi"
                )

                writer.writerow([
                    ticket["ticket_id"],
                    ticket["license_plate"],
                    ticket["vehicle_type"],
                    ticket["entry_time"].strftime("%Y-%m-%d %H:%M:%S"),
                    ticket["exit_time"].strftime("%Y-%m-%d %H:%M:%S")
                    if ticket["exit_time"] else "",
                    ticket["fee"],
                    status
                ])

        return os.path.abspath(filename)
