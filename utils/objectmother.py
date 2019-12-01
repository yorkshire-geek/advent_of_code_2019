class ObjectMother:
    def __init__(self, file_name):
        self.file_name = file_name

    def return_list(self, factory_method):

        result = []
        with open(self.file_name, 'r') as input_file:
            for line in input_file:
                result.append(factory_method(line.strip()))
        input_file.close()

        return result

