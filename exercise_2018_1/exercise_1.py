from utils.objectmother import ObjectMother
from utils.datawrapper import DataWrapper


class Ex1DataWrapper (DataWrapper):

    @staticmethod
    def factory(data):
        return Ex1DataWrapper(data)


if __name__ == "__main__":
    mother = ObjectMother("input.txt")
    list_of_data = mother.return_list(Ex1DataWrapper.factory)
    print(list_of_data)


