"""
Module Tìm Đường Tối Ưu trong Bãi đỗ xe (A* Pathfinding Algorithm).
Chịu trách nhiệm:
- Mô hình hóa bản đồ bãi xe dưới dạng đồ thị lưới (Grid Graph).
- Áp dụng giải thuật A* (A-Star) với hàm Heuristic khoảng cách Manhattan.
- Tìm đường đi ngắn nhất từ ô đỗ xe (ví dụ: 'A01') đến Cổng ra (Exit Gate) an toàn.
"""

import heapq
from typing import List, Tuple, Dict, Optional


class AStarPathfinder:
    """
    Lớp cài đặt thuật toán A* định tuyến phương tiện và thoát hiểm trong bãi đỗ.
    """
    def __init__(self, cols: int = 5, rows: int = 4):
        self.cols = cols
        self.rows = rows
        # Giả định Cổng ra (Exit Gate) nằm ở góc dưới bên phải lưới (Hàng 3, Cột 4)
        self.exit_node = (3, 4)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """
        Sử dụng khoảng cách Manhattan (L1 Norm) làm hàm đánh giá Heuristic:
        h(n) = |x1 - x2| + |y1 - y2|
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Lấy danh sách các nút kề cạnh hợp lệ trong lưới (4 hướng: Trên, Dưới, Trái, Phải)"""
        neighbors = []
        r, c = node
        if r > 0:
            neighbors.append((r - 1, c))
        if r < self.rows - 1:
            neighbors.append((r + 1, c))
        if c > 0:
            neighbors.append((r, c - 1))
        if c < self.cols - 1:
            neighbors.append((r, c + 1))
        return neighbors

    def find_path(self, start_slot_id: str) -> List[Tuple[int, int]]:
        """
        Tìm lộ trình di chuyển tối ưu từ ô đỗ đến Cổng ra:
        - Chuyển đổi mã ô đỗ (ví dụ 'A01', 'B10') thành tọa độ Grid (row, col)
        - Triển khai hàng đợi ưu tiên Priority Queue (Min-Heap)
        - Truy vết và hoàn trả danh sách tọa độ các bước di chuyển
        """
        # Chuyển đổi mã ô thành tọa độ Grid (ví dụ: A01 -> index 0 -> hàng 0, cột 0)
        idx = int(start_slot_id[1:]) - 1
        start_node = (idx // self.cols, idx % self.cols)

        frontier = []
        heapq.heappush(frontier, (0, start_node))
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start_node: None}
        cost_so_far: Dict[Tuple[int, int], int] = {start_node: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == self.exit_node:
                break

            for next_node in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(self.exit_node, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        # Truy vết lại đường đi từ Cổng ra ngược về điểm xuất phát
        current = self.exit_node
        path = []
        while current is not None and current != start_node:
            path.append(current)
            current = came_from.get(current)
        path.append(start_node)
        path.reverse()
        return path
