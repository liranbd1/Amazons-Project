class Queen:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def get_position(self):
        return [self.position[0], self.position[1]]

    def get_color(self):
        return self.color

    def corner_checkup(self, point1, point2, point3):
        if (point1 == " x ") and (point2 == " x ") and (point3 == " x "):
            return False

        elif (point1 != " . ") and (point2 != " . ") and (point3 != " . "):
            return False

        else:
            return True

    def wall_checkup(self, front_row_points, side_points):
        if (
                (front_row_points[0] == " x ")
                and (front_row_points[1] == " x ")
                and (front_row_points[2] == " x ")
                and (side_points[0] == " x ")
                and (side_points[1] == " x ")
        ):
            return False

        elif (
                (front_row_points[0] != " . ")
                and (front_row_points[1] != " . ")
                and (front_row_points[2] != " . ")
                and (side_points[0] != " . ")
                and (side_points[1] != " . ")
        ):
            return False

        else:
            return True

    def is_queen_free(self, board, size):
        px = int(self.position[0])
        py = int(self.position[1])
        size = int(size) - 1

        # Corners
        # Assume queen is in top left corner
        # Bottom spot
        if px == py == 0:
            # Right spot
            right_point = board[px][py + 1]
            # Bottom spot
            bottom_point = board[px + 1][py]
            # Diagonal spot
            diagonal_point = board[px + 1][py + 1]
            return self.corner_checkup(right_point, bottom_point, diagonal_point)

        # Assume queen is in bottom right corner
        elif px == py == size:
            # Top spot
            top_point = board[px - 1][py]
            # Left spot
            left_point = board[px][py - 1]
            # Diagonal spot
            diagonal_point = board[px - 1][py - 1]
            return self.corner_checkup(top_point, left_point, diagonal_point)

        # Assume queen is in top right corner
        elif (px == 0) and (py == size):
            # Left spot
            left_point = board[px][py - 1]
            bottom_point = board[px + 1][py]
            # Diagonal spot
            diagonal_point = board[px + 1][py - 1]
            return self.corner_checkup(left_point, bottom_point, diagonal_point)

        # Assume queen is in bottom left corner
        elif (px == size) and (py == 0):
            # Top spot
            top_point = board[px - 1][py]
            # Right spot
            right_point = board[px][py + 1]
            # Diagonal spot
            diagonal_point = board[px - 1][py + 1]
            return self.corner_checkup(top_point, right_point, diagonal_point)

        # Walls
        # Next to top wall
        elif px == 0:
            # Front row
            front_row_points = [board[1][py - 1], board[1][py], board[1][py + 1]]
            # Sides points
            side_points = [board[px][py - 1], board[px][py + 1]]
            return self.wall_checkup(front_row_points, side_points)

        # Next to bottom wall
        elif px == size:
            # Front row
            front_row_points = [
                board[size - 1][py - 1],
                board[size - 1][py],
                board[size - 1][py + 1],
            ]
            # Sides points
            side_points = [board[px][py - 1], board[px][py + 1]]
            return self.wall_checkup(front_row_points, side_points)

        # Next to left wall
        elif py == 0:
            # Front row
            front_row_points = [board[px - 1][1], board[px][1], board[px + 1][1]]
            # Sides points
            side_points = [board[px + 1][py], board[px - 1][py]]
            return self.wall_checkup(front_row_points, side_points)

        # Next to right wall
        elif py == size:
            # Front row
            front_row_points = [
                board[px - 1][size - 1],
                board[px][size - 1],
                board[px + 1][size - 1],
            ]
            # Side points
            side_points = [board[px + 1][py], board[px - 1][py]]
            return self.wall_checkup(front_row_points, side_points)

        # In a middle space
        else:
            arrow_count = 0
            position_next_to_queen = [
                # Front
                board[px - 1][py - 1],
                board[px - 1][py],
                board[px - 1][py + 1],
                # Back
                board[px + 1][py - 1],
                board[px + 1][py],
                board[px + 1][py + 1],
                # Sides
                board[px][py - 1],
                board[px][py + 1],
            ]

            for position in position_next_to_queen:
                if position == " . ":
                    return True

            return False

    def set_new_position(self, position):
        self.position = position
