#!/usr/bin/env python3

from operator import itemgetter
import networkx as nx
import wikipedia

SEED = "Undertale".title()

STOPS = (
    "Jstor",
    "International Standard Serial Number",
)


todo_lst = [(0, SEED)]  # The SEED is in the layer 0
todo_set = set(SEED)  # The SEED itself
done_set = set()  # Nothing is done yet

F = nx.DiGraph()
layer, page = todo_lst[0]

while layer < 2:
    del todo_lst[0]
    done_set.add(page)
    print(layer, page)  # Show progress

    try:
        wiki = wikipedia.page(page, auto_suggest=False)
    except:
        print("Could not load", page)
        layer, page = todo_lst[0]
        continue

    for link in wiki.links:
        link = link.title()
        if link not in STOPS and not link.startswith("List Of"):
            if link not in todo_set and link not in done_set:
                todo_lst.append((layer + 1, link))
                todo_set.add(link)
            F.add_edge(page, link)
    layer, page = todo_lst[0]

print("{} nodes, {} edges".format(len(F), nx.number_of_edges(F)))

# Eliminate Duplicates
F.remove_edges_from(nx.selfloop_edges(F))

duplicates = [(node, node + "s") for node in F if node + "s" in F]
for dup in duplicates:
    F = nx.contracted_nodes(F, *dup, self_loops=False)
duplicates = [
    (x, y)
    for x, y in [(node, node.replace("-", " ")) for node in F]
    if x != y and y in F
]
for dup in duplicates:
    F = nx.contracted_nodes(F, *dup, self_loops=False)


# Edge attributes
for e, data in F.edges.items():
    if "contraction" in data:
        del F.edges[e]["contraction"]

# Nodes attributes
for n, data in F.nodes.items():
    if "contraction" in data:
        del F.nodes[n]["contraction"]


# Write graph
core = [node for node, deg in dict(F.degree()).items() if deg >= 2]
G = nx.subgraph(F, core)
print("{} nodes, {} edges".format(len(G), nx.number_of_edges(G)))
nx.write_graphml(G, "cna.graphml")
