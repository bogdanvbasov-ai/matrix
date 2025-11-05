class Matrix:
    def __init__(self, matrix: list[list[float]], expanded: list[list[float]] = None):
        for i in range(len(matrix)):
            if len(matrix[i]) != len(matrix[0]):
                raise ValueError("Not a matrix")
        self.is_expanded = False
        if expanded is not None:
            for i in range(len(expanded)):
                if len(expanded[i]) != len(expanded[0]):
                    raise ValueError("Not a expanded matrix")
            self.expanded = expanded
            self.expanded_x = len(expanded)
            self.expanded_y = len(expanded[0])
            self.is_expanded = True
            if self.expanded_x != len(matrix):
                raise ValueError("Impossible matrix size")
        self.x = len(matrix)
        self.y = len(matrix[0])
        new_matrix = []
        for i in range(len(matrix)):
            new_matrix.append([])
            for j in range(len(matrix[0])):
                new_matrix[i].append(matrix[j][i])
        self.matrix = new_matrix


    def __add__(self, other) -> 'Matrix':
        if isinstance(other, int) or isinstance(other, float):
            if self.expanded is not None:
                raise ValueError("Cannot add number with an expanded matrix")
            if self.x == self.y:
                return self + (other * self.first_matrix(self.x))
            else:
                raise ValueError("Not square a matrix")
        elif isinstance(other, Matrix):
            if not self.have_the_same_size(other):
                raise ValueError("Not the same matrix")
            result = [[self.matrix[j][i] + other.matrix[j][i] for j in range(self.x)] for i in range(self.y)]
            if (self.is_expanded and not other.is_expanded) or (not self.is_expanded and other.is_expanded):
                raise ValueError("Cannot add matrix with expanded matrix")
            elif self.is_expanded and other.is_expanded:
                if self.expanded_x == other.expanded_x and self.expanded_y == other.expanded_y:
                    expanded_result = [[self.expanded[j][i] + other.expanded[j][i] for j in range(self.x)] for i in range(self.y)]
                    return Matrix(result, expanded_result)
            return Matrix(result)
        else:
            raise TypeError("Impossible typ")


    def __radd__(self, other) -> 'Matrix':
        return self + other


    def __sub__(self, other) -> 'Matrix':
        return self + (-1) * other


    def __rsub__(self, other) -> 'Matrix':
        return self * (-1) + other


    def __mul__(self, other) -> 'Matrix':
        if isinstance(other, int) or isinstance(other, float):
            result = [[self.matrix[j][i] * other for i in range(self.x)] for j in range(self.y)]
            if self.is_expanded:
                expanded_result = [[self.expanded[j][i] * other for j in range(self.x)] for i in range(self.y)]
                return Matrix(result, expanded_result)
            return Matrix(result)
        elif isinstance(other, Matrix):
            if self.y != other.x:
                raise ValueError("Size is not possible for this operation")
            result = [[0 for _ in range(other.y)] for _ in range(self.x)]
            for x in range(self.x):
                for y in range(other.y):
                    for i in range(self.y):
                        result[x][y] += self.matrix[x][i] * other.matrix[i][y]
            if self.is_expanded and other.is_expanded:
                expanded_result = [[0 for _ in range(other.y)] for _ in range(self.x)]
                if self.expanded_y != other.expanded_x:
                    raise ValueError("Impossible size of expanded matrix")
                for x in range(self.x):
                    for y in range(other.y):
                        for i in range(self.y):
                            expanded_result[x][y] += self.expanded[x][i] * other.expanded[i][y]
                return Matrix(result, expanded_result)
            return Matrix(result)
        else:
            raise TypeError("Impossible typ")


    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Matrix):
            return self * other
        else:
            raise TypeError("Impossible typ")


    def __truediv__(self, other) -> 'Matrix':
        if isinstance(other, Matrix):
            return self * other.inverse_matrix()
        elif isinstance(other, int) or isinstance(other, float):
            return self * (1 / other)
        else:
            raise TypeError("Impossible typ")


    def __rtruediv__(self, other):
        return other * self.inverse_matrix()


    def __eq__(self, other) -> bool:
        if isinstance(other, Matrix):
            if self.have_the_same_size(other):
                for i in range(self.x):
                    for j in range(self.y):
                        if self.matrix[i][j] != other.matrix[i][j]:
                            return False
                for i in range(self.expanded_x):
                    for j in range(self.expanded_y):
                        if self.expanded[i][j] != other.expanded[i][j]:
                            return False
                return True
            else:
                raise SyntaxError("Impossible size")
        else:
            raise TypeError("Impossible Type")


    def __ne__(self, other) -> bool:
        return not self == other


    def __str__(self) -> str:
        s = ""
        for i in range(self.y):
            for j in range(self.x):
                s += str(self.matrix[j][i])
                if j != self.x - 1:
                    s += "\t"
            if self.is_expanded:
                s += "\t|\t"
                for j in range(self.expanded_y):
                    s += str(self.expanded[j][i])
                    if i != self.expanded_y - 1:
                        s += "\t"
            s += "\n"
        return s


    def __getitem__(self, index: int, need_expanded: bool = False):
        if need_expanded:
            return self.expanded[index]
        return self.matrix[index - 1]


    def __setitem__(self, index: int, value: float, need_expanded: bool = False) -> None:
        if need_expanded:
            self.expanded[index - 1] = value
        else:
            self.matrix[index - 1] = value


    def adj(self) -> 'Matrix':
        if self.is_expanded:
            raise ValueError("Cannot do this operation with expanded matrix")
        temp = []
        for i in range(self.x):
            temp.append([])
            for j in range(self.y):
                temp[i].append(self.a(i + 1, j + 1))
        return Matrix(temp)


    def inverse_matrix(self) -> 'Matrix':
        if self.is_expanded:
            raise TypeError("Cannot invert matrix with expanded matrix")
        if self.det()!= 0:
            return self.adj().transposition() / self.det()
        raise


    @staticmethod
    def first_matrix(size: int) -> 'Matrix':
        if size < 0:
            raise TypeError("Impossible size")
        result = list(list())
        for i in range(size):
            result.append([])
            for j in range(size):
                if i == j:
                    result[i].append(1)
                else:
                    result[i].append(0)
        return Matrix(result)


    def transposition(self) -> 'Matrix':
        if self.is_expanded:
            raise TypeError("Cannot transpose matrix with expanded matrix")
        return Matrix([[self.matrix[j][i] for j in range(self.x)] for i in range(self.y)])


    def have_the_same_size(self, other: 'Matrix') -> bool:
        if self.is_expanded and other.is_expanded:
            if self.expanded_x != other.expanded_x or self.expanded_y != other.expanded_y:
                return False
            return True
        elif self.is_expanded or other.is_expanded:
            raise TypeError("Impossible matrix")
        if (self.x != other.x) or (self.y != other.y):
            return False
        return True


    def is_square_matrix(self) -> bool:
        if self.is_expanded:
            raise RuntimeError("Cannot do this operation with expanded matrix")
        if self.x == self.y:
            return True
        return False


    def det(self) -> int:
        if self.is_expanded:
            raise RuntimeError("Cannot do this operation with expanded matrix")
        if not self.is_square_matrix():
            raise TypeError("Impossible size")
        if self.x == 1:
            return self.matrix[0][0]
        return sum(self.matrix[0][i] * self.a(1, i + 1) for i in range(self.x))


    def a(self, x: int, y: int) -> int:
        if self.is_expanded:
            raise RuntimeError("Cannot do this operation with expanded matrix")
        x -= 1
        y -= 1
        if self.x == 1:
            return self.matrix[0][0]
        return self.m(x + 1, y + 1) * ((-1) ** (x + y))


    def m(self, x: int, y: int) -> int:
        if self.is_expanded:
            raise RuntimeError("Cannot do this operation with expanded matrix")
        x -= 1
        y -= 1
        if not self.is_square_matrix():
            raise TypeError("Impossible size")
        if self.x == 1:
            return self.matrix[0][0]
        matrix = list(list())
        real_x = -1
        for i in range(self.x):
            if i == x:
                continue
            real_x += 1
            matrix.append([])
            for j in range(self.y):
                if j == y:
                    continue
                matrix[real_x].append(self.matrix[i][j])
        return Matrix(matrix).det()


    def change_lines(self, first: int, second: int):
        if first > self.x or second > self.x:
            raise ValueError("Impossible x")
        first -= 1
        second -= 1
        for i in range(self.x):
            for j in range(self.y):
                if i == first:
                    self.matrix[first][j], self.matrix[second][j] = self.matrix[second][j], self.matrix[first][j]
        if self.is_expanded:
            for i in range(self.expanded_x):
                for j in range(self.expanded_y):
                    if i == first:
                        self.expanded[first][j], self.expanded[second][j] = self.expanded[second][j], self.expanded[first][j]


    def change_columns(self, first: int, second: int):
        if first > self.y or second > self.y:
            raise ValueError("Impossible y")
        first -= 1
        second -= 1
        for i in range(self.x):
            for j in range(self.y):
                if j == first:
                    self.matrix[i][first], self.matrix[i][second] = self.matrix[i][second], self.matrix[i][first]


    def line_plus_line(self, first: int, second: int, k: float = 1) -> None:
        if first > self.x or second > self.x:
            raise ValueError("Impossible x")
        first -= 1
        second -= 1
        for i in range(self.x):
            for j in range(self.y):
                if i == first:
                    self.matrix[first][j] += self.matrix[second][j] * k
        if self.is_expanded:
            for i in range(self.expanded_x):
                for j in range(self.expanded_y):
                    if i == first:
                        self.expanded[first][j] += self.expanded[second][j] * k


    def colum_plus_column(self, first: int, second: int, k: float = 1) -> None:
        if first > self.y or second > self.y:
            raise ValueError("Impossible y")
        first -= 1
        second -= 1
        for i in range(self.x):
            for j in range(self.y):
                if j == first:
                    self.matrix[i][first] += self.matrix[i][second] * k