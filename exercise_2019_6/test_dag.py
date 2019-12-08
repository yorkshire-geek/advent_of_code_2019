import unittest
from .dag import Dag


class MyTestCase(unittest.TestCase):
    def test_add_child(self):
        dag = Dag()
        dag.add_parent_child("parent", "child")
        self.assertEqual(dag.has_node("parent"), True)
        self.assertEqual(dag.has_node("child"), True)
        self.assertEqual(dag.has_node("should not find me"), False)

    def test_get_children(self):
        dag = Dag()
        dag.add_parent_child("parent", "child1")
        dag.add_parent_child("parent", "child2")
        dag.add_parent_child("parent", "child2")  # add same child twice
        self.assertEqual(len(dag.get_children("parent")), 2)

    def test_get_has_children(self):
        dag = Dag()
        dag.add_parent_child("parent", "child")
        self.assertEqual(dag.has_children("parent"), True)
        self.assertEqual(dag.has_children("child"), False)

    def test_get_descendants(self):
        dag = Dag()
        dag.add_parent_child("parent", "child1")
        dag.add_parent_child("parent", "child2")
        dag.add_parent_child("child1", "grandchild1")
        dag.add_parent_child("child2", "grandchild2")
        dag.add_parent_child("child2", "grandchild3")
        print(dag.get_descendants("parent"))
        self.assertEqual(len(dag.get_descendants("parent")), 5)

    def test_route_to_parent(self):
        dag = Dag()
        dag.add_parent_child("parent", "child1")
        dag.add_parent_child("parent", "child2")
        dag.add_parent_child("child1", "grandchild1")
        dag.add_parent_child("child2", "grandchild2")
        dag.add_parent_child("child2", "grandchild3")
        dag.add_parent_child("grandchild3", "greatgrandchild1")
        self.assertEqual(dag.get_jumps_to_descendant("parent", "greatgrandchild1"), 3)
        self.assertEqual(dag.get_jumps_to_descendant("parent", "child2"), 1)
        # print(dag.get_jumps_as_list("parent", "greatgrandchild1"))

    def test_sample_dag(self):
        dag = Dag()
        dag.add_parent_child("OM", "B")
        dag.add_parent_child("C", "D")
        dag.add_parent_child("B", "C")
        dag.add_parent_child("D", "E")
        dag.add_parent_child("E", "F")
        dag.add_parent_child("B", "G")
        dag.add_parent_child("G", "H")
        dag.add_parent_child("D", "I")
        dag.add_parent_child("E", "J")
        dag.add_parent_child("J", "K")
        dag.add_parent_child("K", "L")

        self.assertEqual(dag.get_total_orbits("OM"), 42)


if __name__ == '__main__':
    unittest.main()


