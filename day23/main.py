import networkx as nx
from ipysigma import Sigma

from utils import read_input

TEST_ANSWER_PART1 = 7
TEST_ANSWER_PART2 = "co,de,ka,ta"


def build_network(lines: list[str]) -> nx.Graph:
    graph = nx.Graph()
    for line in lines:
        left, right = line.split("-")
        graph.add_edge(left, right)

    # visualize it baby
    Sigma(graph, height=1000, start_layout=5).to_html("graph.html")

    return graph


def part1(lines: list[str]) -> int:
    graph = build_network(lines)

    # this could probably be nicer with networkx (triangles?), but meh
    triples_with_t = set()
    for n1 in graph:
        for n2 in graph[n1]:
            all_neighbors = set(graph[n1]).union(set(graph[n2]))
            for n3 in all_neighbors:
                if n3 == n1 or n3 == n2:
                    continue

                if not graph.has_edge(n1, n3) or not graph.has_edge(n2, n3):
                    continue

                if any(comp.startswith("t") for comp in [n1, n2, n3]):
                    triples_with_t.add(frozenset({n1, n2, n3}))

    return len(triples_with_t)


def part2(lines: list[str]) -> str:
    graph = build_network(lines)
    max_clique = max(nx.find_cliques(graph), key=len)
    # print("max", max_clique)
    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
