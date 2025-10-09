import matrizi
matrices = {}
priority = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    ".T": 3,
    ".R": 3,
}


def start():
    hints()
    print("Enter your operation: ", end="")
    inp = input().lower().rstrip()
    while inp != "stop":
        if inp == "new":
            new_matrix = []
            print("Enter matrix name: ", end="")
            name_matrx = input()
            while not is_name_possible(name_matrx) or name_matrx in matrices.keys():
                print("Invalid name. Enter another matrix name: ", end="")
                name_matrx = input()
            print("Enter your matrix. You mast separate the elements with space.")
            line = input()
            while line != "":
                new_matrix.append([float(i) for i in line.rstrip().split(" ")])
                line = input()
            print(new_matrix)
            matrices[name_matrx] = matrizi.Matrix(new_matrix)
        elif inp == "equations":
            print("Enter your equations: ", end="")
            inp = input()
            to_queue(inp)
        else:
            print("Impossible command")
        print("Enter your operation: ", end="")
        inp = input().lower().rstrip()


def hints():
    pass


def to_queue(inp: str):
    inp.rstrip()
    inp += " "
    steak = []
    queue = []
    index = 0
    name = ""
    for i in inp:
        if i == " ":
            break
        if i in "+-/*.":
            if i == "." and inp[index + 1] == "R":
                operation = ".R"
            elif i == "." and inp[index + 1] == "T":
                operation = ".T"
            else:
                operation = i
            if len(steak) == 0:
                steak.append(operation)
            else:
                while priority[steak[-1]] >= priority[operation]:
                    queue.append(steak.pop())
                    if len(steak) == 0:
                        steak.append(operation)
                        break
                else:
                    steak.append(operation)
        elif i == "(":
            steak.append(i)
        elif i == ")":
            for j in steak[::-1]:
                if j != "(":
                    queue.append(steak.pop())
                elif j == "(":
                    steak.pop()
                    break
        else:
            if inp[index - 1] == ".":
                continue
            name += i
            if inp[index + 1] in " +-/*.":
                queue.append(name)
                name = ""
        index += 1
    for i in steak[::-1]:
        queue.append(i)
    make_operation(queue)


def make_operation(queue: list) -> None:
    steak = []
    for i in range(len(queue)):
        if queue[i] == "+":
            steak.append(steak.pop() + steak.pop())
        elif queue[i] == "-":
            temp = steak.pop()
            steak.append(steak.pop() - temp)
        elif queue[i] == "*":
            steak.append(steak.pop() * steak.pop())
        elif queue[i] == "/":
            temp = steak.pop()
            steak.append(steak.pop() / temp)
        elif queue[i] == ".T":
            steak.append(steak.pop().transposition())
        elif queue[i] == ".R":
            steak.append(steak.pop().inverse_matrix())
        else:
            steak.append(matrices[queue[i]])
        print(steak[0])


def is_name_possible(name: str) -> bool:
    if "=" in name or "-" in name or "*" in name or "/" in name or "." in name:
        return False
    return True


def is_line_possible(line: str) -> bool:
    line = line.rstrip() + " "
    index = 0
    is_last_operation = False
    braces_count = 0
    name = ""
    if line[0] in "+-/*.":
        return False
    for i in line:
        if braces_count < 0:
            return False
        if i == " ":
            break
        if i in "+-/*.":
            if is_last_operation:
                return False
            is_last_operation = True
            if i == "." and line[index + 1] != "R":
                return False
            elif i == "." and line[index + 1] != "T":
                return False
        elif line[index - 1] == ".":
            continue
        elif i == "(":
            braces_count += 1
        elif i == ")":
            braces_count -= 1
        else:
            name += i
            if line[index + 1] in " +-/*.":
                if name in matrices.keys():
                    return False
                name = ""
    return True

start()
