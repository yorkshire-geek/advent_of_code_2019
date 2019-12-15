import re
from itertools import permutations, combinations


def add_brackets(equation: str):
    new_equation = "(" + equation.re.split("+/-\\*")

    p = re.compile("[-*+/]")
    for m in p.finditer(new_equation):
        print(str(m.start()) + "()" + str(m.group()))

    return new_equation


if __name__ == '__main__':

    de_duped = set()

    permutations_of_numbers = permutations([3, 3, 8, 8])
    for perm in permutations_of_numbers:
        # print(perm)
        de_duped.add(perm)

    print("--- Numbers")

    # de_duped = set(permutations_to_check)
    for de_dup in de_duped:
        print(de_dup)

    print("--- Operators")

    de_duped_operators = set()
    permutations_of_operators = combinations(["+", "+", "+", "-", "-", "-", "*", "*", "*", "/", "/", "/"], 3)
    for perm in permutations_of_operators:
        de_duped_operators.add(perm)

    # count = 0
    # for de in de_duped_operators:
    #     print(de)
    #     count += 1
    # print(count)

    count = 0
    for numbers in de_duped:
        for operators in de_duped_operators:
            equation1 = "(" + str(numbers[0]) + str(operators[0]) + str(numbers[1]) + ")" + str(operators[1]) + "(" \
                        + str(numbers[2]) + str(operators[2]) + str(numbers[3]) + ")"
            equation2 = "((" + str(numbers[0]) + str(operators[0]) + str(numbers[1]) + ")" + str(operators[1]) \
                        + str(numbers[2]) + ")" + str(operators[2]) + str(numbers[3])
            equation3 = str(numbers[0]) + str(operators[0]) + "((" + str(numbers[1]) + str(operators[1]) + \
                        str(numbers[2]) + ")" + str(operators[2]) + str(numbers[3]) + ")"
            equation4 = str(numbers[0]) + str(operators[0]) + "(" + str(numbers[1]) + str(operators[1]) + \
                        "(" + str(numbers[2]) + str(operators[2]) + str(numbers[3]) + "))"
            equation5 = "(" + str(numbers[0]) + str(operators[0]) + "(" + str(numbers[1]) + str(operators[1]) + \
                        str(numbers[2]) + "))" + str(operators[2]) + str(numbers[3])

            print(str(equation1) + " = " + str(eval(equation1)))
            print(str(equation2) + " = " + str(eval(equation2)))
            print(str(equation3) + " = " + str(eval(equation3)))
            print(str(equation4) + " = " + str(eval(equation4)))
            print(str(equation5) + " = " + str(eval(equation5)))

            count += 5

    print("---" + str(count))

            #
            # # print(equation + " = " + str(eval(equation)))
            # print(new)



