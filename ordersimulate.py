

import itertools
import sys

statistics = {}
unique_node = {}
counter = 0
path_count = 0


class State(object):
    NULL  = -1
    LOAD  = 0
    ADD   = 1
    STORE = 2
    maps = {
        -1: "NULL",
        0: "LOAD",
        1: "ADD",
        2: "STORE"
    }

    @classmethod
    def mapping(cls, t):
        return "(" + cls.maps[t[0]]\
                + ", " + cls.maps[t[1]] + ")"


class MM(object):

    def __init__(self, intial_val):
        self.mm = intial_val

    def __str__(self):
        return f"mm = {self.mm}"


def dfs(cur_state, states, times, mm, cache, max_times, path):
    global path_count
    if times[1] == max_times and times[2] == max_times:
        # if mm.mm != 2:
        #     return None
        statistics[mm.mm] = statistics.get(mm.mm, 0) + 1
        path_count += 1
        np = [State.mapping(state[0]) + ", " + str(state[1]) + "\n" + state[2] + f", pc={path_count}" for state in path[:-1]]
        s = path[len(path) - 1]
        np.append(State.mapping(s[0]) + ", " + str(s[1]) + "\n" + s[2] + f", pc={path_count} ,result = {mm.mm}")
        print_path(np)
        return None

    # save current state data
    tmp_mm = mm.mm
    core2 = cache[2]
    core1 = cache[1]

    for state in states:
        # at condition 2
        if state[0] == cur_state[0] and state[1] == (cur_state[1] + 1) % 3:

            if times[2] == max_times:
                continue

            if state[1] == State.STORE:
                times[2] = times[2] + 1
                mm.mm = cache[2]
            elif state[1] == State.LOAD:
                cache[2] = mm.mm
            elif state[1] == State.ADD:
                cache[2] += 1
            path.append([state, 2, f"mm = {mm.mm} core1 = {cache[1]} core2 = {cache[2]}"])
            dfs(state, states, times, mm, cache, max_times, path)
            path.pop()

            # resume cache and mm
            if state[1] == State.STORE:
                times[2] = times[2] - 1
                mm.mm = tmp_mm
            elif state[1] == State.LOAD:
                cache[2] = core2
            elif state[1] == State.ADD:
                cache[2] -= 1

        # at condition 1
        elif state[0] == (cur_state[0] + 1) % 3 and state[1] == cur_state[1]:
            if times[1] == max_times:
                continue
            if state[0] == State.STORE:
                times[1] = times[1] + 1
                mm.mm = cache[1]
            elif state[0] == State.LOAD:
                cache[1] = mm.mm
            elif state[0] == State.ADD:
                cache[1] += 1
            path.append([state, 1, f"mm = {mm.mm} core1 = {cache[1]} core2 = {cache[2]}"])
            dfs(state, states, times, mm, cache, max_times, path)
            path.pop()

            # resume mm and cache
            if state[0] == State.STORE:
                times[1] = times[1] - 1
                mm.mm = tmp_mm
            elif state[0] == State.LOAD:
                cache[1] = core1
            elif state[0] == State.ADD:
                cache[1] -= 1


def print_path(path):
    global counter
    for node in path:
        if node not in unique_node:
            unique_node[node] = counter
            counter += 1
    for i in range(0, len(path) - 1):
        print("", unique_node[path[i]], "->", unique_node[path[i + 1]], f"[label={i + 1}];")


if __name__ == '__main__':
    sys.stdout = open("graph.dot", 'w+')
    print("digraph AST {")
    state_1 = [State.NULL, State.LOAD, State.ADD, State.STORE]
    state_2 = [State.NULL, State.LOAD, State.ADD, State.STORE]
    states = list(itertools.product(state_1, state_2))
    dfs((State.NULL, State.NULL), states, {1: 0, 2: 0}, MM(0), {1: 0, 2: 0}, 2, [[(State.NULL, State.NULL), 0, "mm = 0 core1 = 0 core2 = 0"]])
    for (key, val) in unique_node.items():
        if "result = 2" in key:
            print(val, "[label=\"", key, "\", style=filled, color=red];")
        elif "result" in key:
            print(val, "[label=\"", key, "\", style=filled, color=palegreen];")
        else:
            print(val, "[label=\"", key, "\"];")

    print("}")
    # s = sum(statistics.values())
    # for (key, val) in statistics.items():
    #     print(f"{key = } {val = }\trate = {val / s}")
