from queue import SimpleQueue

def earliest_ancestor(ancestors, starting_node):
    # create adjacency list mapping each child to their parents
    parents = {}
    for parent, child in ancestors:
        values = parents.setdefault(child, [])
        values.append(parent)

    # default: no parent found
    earliest = -1

    # ensure initial child has a parent
    if starting_node in parents:
        # track parentage
        lineages = []
        # initialze queue
        queue = SimpleQueue()
        queue.put([starting_node])
        # begin breadth first search
        while not queue.empty():
            # get current parentage line
            lineage = queue.get()
            # looking for parents of last child in line
            child = lineage[-1]
            # if no known parents (not in dictionary or parent list is empty)
            if child not in parents or not parents[child]:
                # store complete lineage
                lineages.append(lineage)
                # look no further
                continue
            # has parents, so for each known parent
            for parent in parents[child]:
                # append parent to current lineage
                new_lineage = lineage + [parent]
                # queue updated lineage to search for further parents
                queue.put(new_lineage)

        # find furthest ancestor (last entry in longest lineage)
        # store as list to get the lowest numbered from oldest generation
        oldest = []
        max_generations = 0
        for lineage in lineages:
            generations = len(lineage)
            if generations > max_generations:
                max_generations = generations
                oldest = [lineage[-1]]
            elif generations == max_generations:
                oldest.append(lineage[-1])
        
        earliest = min(oldest)

    return earliest