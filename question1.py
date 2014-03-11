from sets import Set



def main():
    # this seems like a fairly reasonable way to represent states and transitions
    # to me.
    state = [None, None, None, None, None, None, None, None, None]
    state[0] = [("b",Set([4])), ("E",Set([1]))]
    state[1] = [("a",Set([2])), ("b",Set([4])), ("E",Set([0]))]
    state[2] = [("a",Set([3,4])), ("b",Set([6]))]
    state[3] = [("a",Set([5]))]
    state[4] = [("a",Set([5])), ("b",Set([7])), ("E",Set([8]))]
    state[5] = [("a",Set([8])), ("b",Set([8])), ("E",Set([6,8]))]
    state[6] = [("a",Set([3])),("E",Set([8,5]))]
    state[7] = [("a",Set([6])), ("b",Set([2]))]
    state[8] = []

    init_states = [0, 1]
    goal_states = [4, 5]

    # create a set of e_closed state sets
    e_closed_states = Set()
    for s in range(0,9):
        e_closed_states.add(frozenset(e_close(state, s, [])))

    dfa = {}
    # now for each e_closed_state we want to run through each input and 
    # figure out which state sets they are going to. 

    added = True

    # a little inconvenient, since it will loop through sets that it's already
    # checked before
    while(added):
        added=False
        new_states = Set()

        # do a
        for s in e_closed_states:
            dfa[s] = []
            for n in s:
                go_to_states = go_to(state, n, "a")
                if len(go_to_states) > 0:

                    # need to check to see if we already have an a entry
                    # if we do, we'll be combing the two a entries into one
                    # state set
                    new_state = Set()
                    new_state = new_state.union(go_to_states)

                    modified = None    # used to make sure we can have more
                    count = 0          # than one "a"
                    for a_transition in dfa[s]:
                        if a_transition[0] == "a":
                            # we already have an a here
                            new_state = new_state.union(a_transition[1])
                            modified = count
                        count += 1

                    new_state = frozenset(new_state) # freeze the set

                    if modified is not None:
                        dfa[s][modified] = ("a", new_state)

                    # we need to add new sets to the e_closed_states set if 
                    # we haven't seen this state set before
                    if new_state not in e_closed_states:
                        new_states.add(new_state)
                        added=True

                    # add this to the dfa transition dictionary
                    # there is a chance that this was already done for us
                    # by trying to accomplish multiple transitions
                    if modified is None:
                        dfa[s].append(("a", new_state))


        # do b
        for s in e_closed_states:
            for n in s:
                go_to_states = go_to(state, n, "b")
                if len(go_to_states) > 0:
                    # need to check to see if we already have an a entry
                    # if we do, we'll be combing the two a entries into one
                    # state set
                    new_state = Set()
                    new_state = new_state.union(go_to_states)

                    modified = None    # used to make sure we can have more
                    count = 0          # than one "b"
                    for a_transition in dfa[s]:
                        if a_transition[0] == "b":
                            new_state = new_state.union(a_transition[1])
                            a_transition = ("b", new_state)
                            modified = count
                        count += 1

                    new_state = frozenset(new_state) # freeze the set
                    if modified is not None:
                        dfa[s][modified] = ("b", new_state)

                    # we need to add new sets to the e_closed_states set if 
                    # we haven't seen this state set before
                    if new_state not in e_closed_states:
                        new_states.add(new_state)
                        added=True

                    # lets add this to the dfa transition dictionary now
                    if modified is None:
                        dfa[s].append(("b", new_state))


        for new in new_states:
            e_closed_states.add(frozenset(new))


    # output the epsilon closure for the assignment question
    print "EPSILON CLOSURE FOR GIVEN STATES"
    for i in range(0, len(state)):
        print "e_close(%s) = %s" % (i, e_close(state, i, []))


    # output the start state for the DFA
    print
    print "INITIAL STATE" 

    # start state will be a union of the e_closures of the given
    # initial states
    dfa_start = Set()
    for i in init_states:
        dfa_start = dfa_start.union(e_close(state, i, []))

    print list(dfa_start)
    print
    # output the final states for the dfa
    # this will be all states that contain the final state
    print "FINAL STATES"

    for i in goal_states:
        for s in e_closed_states:
            if i in s:
                print list(s)
    print

    # time to print out the transitions. I'll try to keep this pretty... somehow
    print "TRANSITIONS"


    print "%-20s %-20s %-20s" % ("State", "a", "b")
    for key in dfa:
        if len(dfa[key]) > 0:
            print "%-20s %-20s %-20s" % (list(key), print_a(dfa[key]), print_b(dfa[key]))
        else:
            print "%-20s %-20s %-20s" % (list(key), "--", "--")

# find the a tuple and print it if it exists
def print_a(row):
    for t in row:
        if t[0] == "a":
            return list(t[1])
    return "--"
# find the b tuple and return it if it exists
def print_b(row):
    for t in row:
        if t[0] == "b":
            return list(t[1])

    return "--"
# do a little bit of recursing to figure out the epsilon closure for the given
# number. This should be fine for most problems, but python has a little bit
# of an issue with recursion
def e_close(state, num, visited):
    if num not in visited:
        visited.append(num)
        for i in state[num]:
            if i[0] == 'E':
                for j in i[1]:
                    e_close(state, j, visited)
    return visited

# given a state and a character return the states that this state will go to
def go_to(state, num, character):
    out_list = []
    for i in state[num]:
        if i[0] == character:
            for j in i[1]:
                out_list.append(j)

    final_set = Set()
    for out in out_list:
        # get the e_close set for each transitioned to state
        temp_set = Set(e_close(state, out, []))

        # add new elements to the final set
        final_set = final_set.union(temp_set)

    return frozenset(final_set)


def check_for_key(state, key):
    for i in state:
        if i[0] == key:
            return True
    return False
if __name__ == "__main__":
    main()





