class Dag:
    def __init__(self):
        self._dictionary = {}
        self._cnt = 0

    def add_parent_child(self, parent: str, child: str):
        self._add_node_to_dict_if_doesnt_exist(parent)
        self._add_node_to_dict_if_doesnt_exist(child)

        set_of_children = self.get_children(parent)
        set_of_children.add(child)

    def has_node(self, node_name) -> bool:
        return node_name in self._dictionary

    def get_children(self, node):
        return self._dictionary[node]

    def has_children(self, node) -> bool:
        return len(self.get_children(node)) > 0

    def _add_node_to_dict_if_doesnt_exist(self, node):
        if node not in self._dictionary:
            self._dictionary[node] = set()

    def get_descendants(self, node) -> set:
        self._cnt = 1
        result = set()
        self._get_descendants_with_collector(node, result)
        return result

    def _get_descendants_with_collector(self, node, collector) -> None :
        if not self.has_children(node):
            return
        else:
            for child in self.get_children(node):
                collector.add(child)
                self._get_descendants_with_collector(child, collector)

    def get_jumps_to_descendant(self, ancestor, descendant) -> int :
        result = 0
        node = ""
        while node != ancestor:
            result += 1
            for node in self._dictionary:
                if descendant in self.get_children(node):
                    descendant = node
                    break
        return result

    def get_jumps_as_list(self, ancestor, descendant) -> list():
        result = []
        node = ""
        while node != ancestor:
            result.append(node)
            for node in self._dictionary:
                if descendant in self.get_children(node):
                    descendant = node
                    break
        return result

    def get_total_orbits(self, primary_body) -> int :
        result = 0
        all_descendants = self.get_descendants(primary_body)
        for child in all_descendants:
            result += self.get_jumps_to_descendant(primary_body, child)
        return result


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


# route to YOU: ['TS7', 'SXW', 'G8B', 'PC1', 'BT3', 'QPY', '8TL', 'P49', 'QCH', 'SRY', '19D', '8S4', 'FDG', 'RNW', 'N7H', '9T2', 'XBC', '4PQ', 'VG5', '1PH', '3X9', 'J92', 'JHZ', 'W4T', '4ST', 'MD8', '8C4', 'WQ1', 'CN5', 'F18', 'KXM', 'Y7R', '887', 'NL6', '7R8', '18G', '5L8', 'T79', 'HR6', '1Z9', 'CWB', 'T2P', 'XYD', '5MK', 'DZ2', 'W54', 'K8Q', 'KGF', 'N3J', '19N', 'H7Q', 'BYR', 'D7F', 'V85', 'RPS', 'JC1', 'NPM', '32C', '5V2', '3JS', '4CG', 'TQW', '2RG', 'N2F', 'BBK', 'L2J', 'JGT', 'HDW', 'XJ1', '7SK', 'P31', '7YQ', '9Q3', 'RDR', 'PDW', '1DD', 'N5J', 'T3B', 'X3J', 'S5D', '3BZ', 'KL9', 'CV9', 'NSF', 'HBX', '5G1', 'NRX', 'YZV', '9HZ', 'S9Q', 'QTX', 'NGT', '557', '7RZ', 'RVY', '2BG', '4LC', 'XN3', 'N9T', 'C4Z', 'C62', 'CG5', 'BQZ', 'VTX', 'LS5', '2JS', '5K8', 'LCQ', '12J', 'BTR', 'JW6', 'YBT', 'KDX', 'DYQ', 'Y29', 'WP2', 'RT8', '3VJ', 'YC3', 'SQ9', 'G8N', 'ZDM', 'RDQ', 'KHX', 'Y4L', '9WJ', 'FKM', 'BLW', 'KL5', 'F6J', '1TF', 'SZF', '3KK', '2N2', 'TNP', 'W4M', '9XL', 'B96', 'BWL', 'V2J', 'KLC', 'DLH', '49R', 'JKS', 'PZG', 'SXM', 'S8Z', 'CGY', 'QNP', 'SN2', 'K8P', 'T3K', 'WXT', '37G', 'MQZ', 'WSY', 'X8D', '6CP', '1WF', 'YMR', 'J16', 'YP5', '2V2', '7Z7', 'QW4', '28L', 'QJJ', 'HH8', '513', 'JWB', 'YRF', 'G89', '5K6', 'ZM8', 'NBL', '4PT', '49L', 'J9T', 'V73', '5Z2', '13Z', 'ZQK', 'NW4', 'BR4', 'P99', 'K2C', 'SG1', 'NCH', 'RVR', 'VNM', '74B', 'WYD'
#                      route to SAN: ['', 'NWW', 'HYJ', '8HX', 'D2F', 'X6L', 'TWT', 'P1Z', 'J7Z', 'M2P', 'XFK', 'XBH', 'LG1', 'FXT', 'LG8', 'RQ1', 'YYN', '1KL', 'GC1', '7T6', 'JFS', 'YT6', 'H4D', 'VHH', 'CLL', 'VYX', 'RKV', 'WC5', '9VL', 'N3C', 'NL9', 'XHJ', 'CQL', 'BS4', 'P9C', 'D5F', 'VPZ', 'K38', 'F2Y', '4MX', '5BW', '66K', 'BG9', 'MXL', 'C6X', '2RT', 'KNG', 'HDN', 'LS9', 'TQP', 'NPY', '9VB', '23C', 'QLF', 'Q29', 'VXB', 'FM2', 'CBH', 'Q98', '6PS', 'NVB', 'B9Z', 'S98', 'R53', '6DP', 'J2S', 'QS6', '7RN', 'CN2', 'XGH', 'B9D', 'QNH', 'NPV', '2SQ', '297', '95C', 'JK4', 'VYF', 'NCR', 'YN2', '78B', '5NX', 'JYY', '8WS', 'JXZ', '9VD', '457', '4W4', '2KP', 'JR7', 'LDK', 'CVN', 'TRW', 'ZGT', 'PR6', 'JDR', 'RR4', 'FZ1', 'M8V', 'TCD', 'CNJ', 'VZX', 'KY2', 'PQC', '1GW', 'P3X', '6G3', 'CTK', 'F6K', 'GV2', 'P78', '8TP', 'HCB', 'ZJV', '6GN', 'XV7', '9MC', 'Z8D', 'NWG', 'ZD2', '6CD', 'KR9', 'S2G', 'MFS', 'DK1', 'C75', 'BL5', '7HS', 'HVX', 'XYQ', 'MBW', 'JV3', 'QPL', 'PDN', 'BPR', 'TK5', 'VC3', 'ZSC', 'KG7', '82B', 'FRL', '4B7', 'BKD', 'T7H', 'NLQ', 'FQQ', 'T1T', 'W4V', 'LGD', 'YX5', 'LL6', 'LKP', '8FN', 'C8V', '3SR', '34Y', '92Q', '78F', 'W2L', 'RC8', '6HH', 'PT7', 'BMN', 'M82', 'VLH', 'LVJ', 'NJ8', 'KZH', '6WP', 'PTR', '189', 'GJH', '5NF', 'BSD', '8HN', 'CXC', 'WFH', 'DSQ', 'VX7', '4Q7', '8Y7', 'SD1', 'KS7', 'BR6', 'B75', 'BW5', 'WWR', '3D6', 'MGZ', 'WYD',
