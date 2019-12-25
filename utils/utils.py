def read_file():
    input_file = open("input.txt", "r")
    if input_file.mode == 'r':
        return input_file.read()