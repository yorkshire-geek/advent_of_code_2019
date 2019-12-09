from exercise_2019_6.dag import Dag
from utils.objectmother import ObjectMother
from utils.datawrapper import DataWrapper


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

    # Question 1
    # print("answer: %d" % dag.get_total_orbits("COM"))

    # Question 2
    you_to_wyd = dag.get_jumps_to_descendant("WYD", "YOU")
    san_to_wyd = dag.get_jumps_to_descendant("WYD", "SAN")

    print("total number of orbits: %d" % (you_to_wyd + san_to_wyd - 2))
