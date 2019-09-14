class Node():
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children

    def getDict(self, level=0) -> dict:
        lines = []
        for child in self.children:
            if isinstance(child, Node):
                lines.append({str(child.value) : list(child.getDict(level+1))})
            else:
                lines.append(child)

        if level == 0:
            return { str(self.value) : list(lines)}
        else:
            return lines
        
    def __str__(self, level=0) -> str:
        ret = "├" + "───" * level + " " + repr(self.value) + "\n"
        for child in self.children:
            if isinstance(child, Node):
                ret += child.__str__(level+1)
            else:
                ret += "├" + "───" * (level+1) + " " + str(child) + "\n"
        return ret

    def __repr__(self):
        return '<tree node object>'

if __name__ == "__main__":
    root = Node("a", [Node("b", [1,2,Node("c", [2,3,4,5])]), 4, 5, 6])
    print(root.getDict())
