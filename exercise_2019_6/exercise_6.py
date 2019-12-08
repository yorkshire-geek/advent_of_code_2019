from utils.objectmother import ObjectMother
from utils.datawrapper import DataWrapper
from .dag import Dag


class Ex6DataWrapper (DataWrapper):

    @staticmethod
    def factory(data):
        return Ex6DataWrapper(data)

    def get_parent(self) -> str:
        return self.data.split(")")[0]

    def get_child(self) -> str:
        return self.data.split(")")[1]


if __name__ == "__main__":
    list_of_data = ObjectMother("input.txt").return_list(Ex6DataWrapper.factory)

    dag = Dag()
    for item in list_of_data:
        dag.add_parent_child(item.get_parent(), item.get_child())

    print("answer: %d" % dag.get_jumps_to_descendant("COM"))
