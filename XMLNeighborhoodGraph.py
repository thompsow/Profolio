from xml.etree import ElementTree

class graph_node:
    def __init__(self, node):
        self._node = node
        self.children = []
    def __str__(self):
        if self._node.tag == 'block':
            tab = '  '
        elif self._node.tag == 'house':
            tab = '     '
        elif self._node.tag == 'car':
            tab = '       '
        else:
            tab = ''
        return tab + self._node.tag + ' ' + str(self._node.attrib)
    def add_child(self, child):
        self.children += (child,)
    def get_node(self):
        return self._node
    __repr__ = __str__
        
class NeighborhoodGraph(object):
    def __init__(self, neighborhood_xml_file):
        self._tree = ElementTree.parse(neighborhood_xml_file)
        self._elem_type = type(self._tree.getroot())
        self._neighborhood = None
        self._block = None
        self._house = None
        self.car_types = []
        self.create_graph()
        self.print_graph()
        print "*** car types ***\n%s" % str(self.car_types)
        
    def create_graph(self, node=None):
        if node == None: # initial call
            node = self._tree.getroot()
            self.car_types = []
            if self._neighborhood:
                del self._neighborhood
        else:
            if not type(node) == self._elem_type:
                return # end or invalid node
        if node.tag == 'neighborhood': # root element
            self._neighborhood = graph_node(node)
            for child in node:
                self.create_graph(child) # recursive call
        if node.tag == 'block': # block node
            self._block = graph_node(node)
            self._neighborhood.add_child(self._block)
            for child in node:
                self.create_graph(child) # recursive call
        if node.tag == 'house': # house node
            self._house = graph_node(node)
            self._block.add_child(self._house)
            for child in node:
                self.create_graph(child) # recursive call
        if node.tag == 'car':   # car node
            self._house.add_child(graph_node(node))
            if not node.attrib['type'] in self.car_types:
                self.car_types += (node.attrib['type'],)
    
    def print_graph(self, node=None):
        if self._neighborhood:
            if node == None: # initial call
                node = self._neighborhood
                print node
            for child in node.children:
                print child
                self.print_graph(child) # recursive call
    
    def find_car(self, car='', node=None):
        if self._neighborhood:
            if node == None: # initial call
                node = self._neighborhood
            for child in node.children:
                if child.get_node().tag == 'house':
                    for this_car in child.children:
                        if this_car.get_node().attrib['type'] == car:
                            print "Found a %s at: %s house on %s %s street" % \
                                  (car, child.get_node().attrib['name'],
                                   child.get_node().attrib['address'],
                                   node.get_node().attrib['street'])
                self.find_car(car, child) # recursive call
                            
if __name__ == '__main__':
    temp = NeighborhoodGraph("neighborhood.xml")
    for car in temp.car_types:
        print "Find all %s cars in neighborhood:" % car
        temp.find_car(car)
    del temp
