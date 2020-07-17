from queue import LifoQueue

# http://code.activestate.com/recipes/579103-python-addset-attributes-to-list/
class ParentChildList(list):
    def __new__(self, *args, **kwargs):
        return super(ParentChildList, self).__new__(self, args, kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)
        self.parents = set()
        self.children = set()
        for parent, child in self:
            self.parents.add(parent)
            self.children.add(child)

    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

    def has_parent(self, person):
        return person in self.children

    def get_parents(self, person):
        parents = []
        for parent, child in self:
            if person == child:
                parents.append(parent)
        return parents
    
    def lineage(self, person):
        if not self.has_parent(person):
            return -1
        lineages = {}
        queue = LifoQueue()
        queue.put([person])
        while not queue.empty():
            lineage = queue.get()
            person = lineage[-1]
            if not self.has_parent(person):
                temp = lineages.setdefault(len(lineage), [])
                temp.append(lineage)
                continue
            for parent in self.get_parents(person):
                queue.put(lineage + [parent])
        
        return lineages

    def earliest_ancestors(self, person):
        lineages = self.lineage(person)
        return -1 if lineages == -1 else [
            lineage[-1] for lineage in lineages[max(lineages)]
        ]


def earliest_ancestor(ancestors, starting_node):
    pcl = ParentChildList(*ancestors)
    earliest = pcl.earliest_ancestors(starting_node)
    return -1 if earliest == -1 else min(earliest)
