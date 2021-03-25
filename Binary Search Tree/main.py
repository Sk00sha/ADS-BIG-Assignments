from typing import *
import numpy as np
import pandas as pd
# from tqdm.auto import tqdm


class Shared:
    def __init__(self) -> None:
        self.full_dict: Dict[str, int] = {}
        self.my_dict: Dict[str, float] = {}
        self.sum_of_all_words: int = 0
        self.total_p: float = 0.0
        self.total_q: float = 0.0
        self.p_list: List[float] = []
        self.q_list: List[float] = []


def read_file(filepath: str, shared: ClassVar) -> None:
    with open(filepath) as f:
        for content in f:
            content = content.strip().split(' ')
            shared.sum_of_all_words += int(content[0])
            shared.full_dict[str(content[1])] = int(content[0])
    shared.full_dict = dict(sorted(shared.full_dict.items()))
    with open(filepath) as f:
        for content in f:
            content = content.strip().split(' ')
            if int(content[0]) > 50000:
                shared.my_dict[str(content[1])] = int(content[0]) / shared.sum_of_all_words
                shared.total_p += int(content[0]) / shared.sum_of_all_words
            else:
                break
    shared.my_dict = dict(sorted(shared.my_dict.items()))
    for key, val in shared.my_dict.items():
        shared.p_list.append(val)


def write_to_file(filepath: str, print_dict: Dict) -> None:
    f = open(filepath, "w")
    for key, value in print_dict.items():
        f.write(f'{key:10}: {value}\n')
    f.close()


def calc_q(shared: ClassVar) -> None:
    tmp: int = 0
    for key, freq in shared.full_dict.items():
        if freq > 50000:
            shared.q_list.append(tmp / shared.sum_of_all_words)
            tmp = 0
        else:
            tmp += freq

    shared.q_list.append(tmp / shared.sum_of_all_words)

    tmp = 0
    for num in shared.q_list:
        tmp += num
    shared.total_q = tmp


def optBST(p: List[float], q: List[float]) -> Any:
    P: List[float] = p
    Q: List[float] = q
    n: int = len(P)

    p = pd.Series(P, index=range(1, n + 1))
    q = pd.Series(Q)

    e = pd.DataFrame(np.diag(Q), index=range(1, n + 2))
    w = pd.DataFrame(np.diag(Q), index=range(1, n + 2))
    root = pd.DataFrame(np.zeros((n, n)), index=range(1, n + 1), columns=range(1, n + 1))

    for k in range(1, n + 1):
        for i in range(1, n - k + 2):
            j = i + k - 1
            e.at[i, j] = np.inf
            w.at[i, j] = w.at[i, j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                t = e.at[i, r - 1] + e.at[r + 1, j] + w.at[i, j]
                if t < e.at[i, j]:
                    e.at[i, j] = t
                    root.at[i, j] = r

    # print(w)

    return e, root.astype(int)


def num_of_comparisons(word, root, keys: List[str]) -> int:
    depth: int = 0
    i: int = 1
    len_keys = len(keys)
    print(root[i, len_keys] - 1)
    while i <= len_keys:
        depth += 1
        print(root[i, len_keys] - 1)
        current_node = keys[root.at[i, len_keys] - 1]
        if current_node == word:
            print("found " + word + " - depth " + str(depth))
            return depth
        elif word < current_node:
            len_keys = root.at[i, len_keys] - 1
        elif word > current_node:
            i = root.at[i, len_keys] + 1
    print("word " + word + " not found")
    return depth


def run(filename: str) -> None:
    shared = Shared()
    read_file(filename, shared)
    write_to_file('over50000.txt', shared.my_dict)

    calc_q(shared)

    write_to_file('all.txt', shared.full_dict)

    p = shared.p_list
    q = shared.q_list

    e, root = optBST(p, q)

    e.to_csv('e.csv', index=False, header=False)
    root.to_csv('root.csv')

    key_list = list(shared.my_dict.keys())
    print(len(key_list))

    print()

    while True:
        word: str = input("insert key: ")
        num_of_comparisons(word, root, key_list)


if __name__ == '__main__':
    run('dictionary.txt')
