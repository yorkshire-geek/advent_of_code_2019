def check_repeating(input_number: int) -> bool:
    number_as_string = str(input_number)
    return number_as_string[0] == number_as_string[1] \
        or number_as_string[1] == number_as_string[2] \
        or number_as_string[2] == number_as_string[3] \
        or number_as_string[3] == number_as_string[4] \
        or number_as_string[4] == number_as_string[5]


def check_ascending(input_number: int) -> bool:
    number_as_string = str(input_number)
    return int(number_as_string[0]) <= int(number_as_string[1]) <= int(number_as_string[2]) <= \
        int(number_as_string[3]) <= int(number_as_string[4]) <= int(number_as_string[5])


def check_repeating_with_extra_rules(input_number: int) -> bool:
    number_str = str(input_number)

    condition_nnx___ = number_str[0] == number_str[1] and number_str[1] != number_str[2]
    condition_xnnx__ = number_str[1] == number_str[2] and number_str[0] != number_str[1] and number_str[2] != number_str[3]
    condition__xnnx_ = number_str[2] == number_str[3] and number_str[1] != number_str[2] and number_str[3] != number_str[4]
    condition___xnnx = number_str[3] == number_str[4] and number_str[2] != number_str[3] and number_str[4] != number_str[5]
    condition____xnn = number_str[4] == number_str[5] and number_str[3] != number_str[4]

    return condition_nnx___ or condition_xnnx__ or condition__xnnx_ or condition___xnnx or condition____xnn


if __name__ == '__main__':
    min_val = 136760
    max_val = 595730

    count = 0
    for password_code in range(min_val, max_val):
        if check_ascending(password_code) and check_repeating(password_code):
            count += 1

    print("--- ")
    print('Question 1: %d' % count)

    count = 0
    for password_code in range(min_val, max_val):
        if check_ascending(password_code) and check_repeating_with_extra_rules(password_code):
            count += 1

    print("Question 2: %d" % count)