
def closure(set: set, term) -> set:
    pass
def goto(set: set) -> set:
    pass

def canonical_collection(initial_state, terminals, non_terminals):
    canonical_collection = set()

    terms = terminals.union(non_terminals)

    s0 = closure([initial_state])
    canonical_collection.add(s0)
    i = 0

    while i < len(canonical_collection):
        s = canonical_collection[i]

        canonical_collection.union({goto(s, term) for term in terms if len(goto(s, term)) != 0})
