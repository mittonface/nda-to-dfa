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

    new_thing = []
    for i in range(9):
        e_closure = e_close(state, num, [])
        

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

def check_for_key(state, key):
    for i in state:
        if i[0] == key:
            return True
    return False
if __name__ == "__main__":
    main()





