import csv, pandas as pd
from .tsp_visualization import plot_route

def rebuild_order_from_arcs(arcs):
    outs = {}
    nodes = set()
    for i, j in arcs:
        outs[i] = j
        nodes.add(i); nodes.add(j)
    start = next(iter(nodes))
    order = [start]
    while len(order) < len(nodes):
        order.append(outs[order[-1]])
    order.append(start)
    return order

if __name__ == "__main__":
    df = pd.read_excel("data/f1_tracks.xlsx")
    idx = {c: i for i, c in enumerate(df["City"])}
    rows = list(csv.reader(open("ampl/solution_arcs.csv", newline="", encoding="utf-8")))
    if rows and rows[0] and rows[0][0].lower().startswith("city"):  # drop header if any
        rows = rows[1:]
    order = rebuild_order_from_arcs(rows)
    path = [idx[c] for c in order]
    plot_route(df, path, title="AMPL TSP Route (MTZ)")
