import matrizi
matrices = dict()
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
    inp = input().lower()
    while inp != "stop":
        if inp == "new":
            new_matrix = []
            print("Enter matrix name: ", end="")
            name_matrx = input()
            print("Enter your matrix. You mast separate the elements with space.")
            line = input()
            while line != "":
                new_matrix.append([int(i) for i in line.rstrip().split(" ")])
                line = input()
            print(new_matrix)
            matrices[name_matrx] = matrizi.Matrix(new_matrix)
        elif inp == "equations":
            print("Enter your equations: ", end="")
            inp = input()
            to_queue(inp)
        else:
            print("Impossible command")
        inp = input().lower()


def hints():
    pass


def to_queue(inp: str):
    inp.rstrip()
    inp += " "
    print(inp)
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
    return queue


print(to_queue("a*b+c.T"))
