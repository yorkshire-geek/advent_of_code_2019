import itertools


def read_file():
    input_file = open("input.txt", "r")
    if input_file.mode == 'r':
        return input_file.read()


def return_layers(contents: str, width: int, height: int) -> []:
    # TODO work out how to do this pythonistically
    #
    layers_count = int(len(contents)/(width*height))
    result_layers = []
    for layer in range(layers_count):
        rows = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(contents[(layer * width * height) + (y * width) + x])
            rows.append(row)
        result_layers.append(rows)

    return result_layers


def get_display_layer(layers: [], width: int, height : int):

    result = []
    for y in range(height):
        result.append([])
        for x in range(width):
            result[y].append([])
            for n in range(len(layers)):
                if layers[n][y][x] in {'0', '1'}:
                    result[y][x] = layers[n][y][x]
                    break

    return result


def question_1(layers: []):
    # Idiomatic way?
    #
    # layer = min((layer.count('0'), layer) for layer in layers)
    # print(layer)
    # print(layer.count('0'))
    # print(list(itertools.chain(*layer).count('0')
    # print(list(itertools.chain(*layers[layer])).count('0'))

    # print("list: has [%d] [%d] [%d]" % (layer.count("0"), layer.count("1"), layer.count("2")))
    # print("---")

    flattened_layers = []
    min_layer = {"layer": -1, "value": 10000}
    for n in range(len(layers)):
        flat_layer = list(itertools.chain(*layers[n]))
        flattened_layers.append(flat_layer)
        if flat_layer.count("0") < min_layer["value"]:
            min_layer["value"] = flat_layer.count("0")
            min_layer["layer"] = flat_layer

    print("layer: has zero count: [%d] 1s count [%d] 2s count [%d]. Code is [%d]" %
            (min_layer["layer"].count("0"), min_layer["layer"].count("1"), min_layer["layer"].count("2"),
                min_layer["layer"].count("1")* min_layer["layer"].count("2")))


def question_2(layers : []):
    display_layer = get_display_layer(layers, 25, 6)
    for line in display_layer:
        line_to_print = ""
        for char in line:
            if char == '0':
                line_to_print += ' '
            elif char == '1':
                line_to_print += u"\u2588"
        print(line_to_print)


if __name__ == '__main__':
    input_string = read_file()
    print("Start with input of size [%d]" % len(input_string))
    input_layers = return_layers(input_string, 25, 6)

    print("Question 1 ----")
    question_1(input_layers)

    print("Question 2 ----")
    question_2(input_layers)
