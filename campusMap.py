import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import ttk, messagebox

#create edges
G = nx.Graph()
nodes = ["Perkins Library", "Duke Chapel", "Bryan Center", "West Union", "Page", "Allen", 
         "Social Sciences", "Reuben Cooke", "Old Chem", "Bostock", "Languages", "Penn", 
         "Wellness", "Wilson", "Gross Hall", "BioSci", "French", "Physics", "LSRC"]
G.add_nodes_from(nodes)

G.add_edge("West Union", "Page", normal_weight=1)  # not accessible
G.add_edge("West Union", "Perkins Library", normal_weight=1, accessible_weight=1)
G.add_edge("Perkins Library", "Duke Chapel", normal_weight=1, accessible_weight=2)
G.add_edge("Page", "Duke Chapel", normal_weight=1, accessible_weight=1)
G.add_edge("West Union", "Allen", normal_weight=2, accessible_weight=2)
G.add_edge("Page", "Bryan Center", normal_weight=2)  # not accessible
G.add_edge("West Union", "Bryan Center", normal_weight=1, accessible_weight=1)
G.add_edge("Duke Chapel", "Bryan Center", normal_weight=2, accessible_weight=4)
G.add_edge("Perkins Library", "Languages", normal_weight=1, accessible_weight=1)
G.add_edge("Perkins Library", "Allen", normal_weight=1, accessible_weight=1)
G.add_edge("Perkins Library", "Social Sciences", normal_weight=1, accessible_weight=1)
G.add_edge("Allen", "Social Sciences", normal_weight=1, accessible_weight=1)
G.add_edge("Social Sciences", "Reuben Cooke", normal_weight=1, accessible_weight=1)
G.add_edge("Languages", "Old Chem", normal_weight=1, accessible_weight=1)
G.add_edge("Languages", "Social Sciences", normal_weight=1, accessible_weight=1)
G.add_edge("Reuben Cooke", "Old Chem", normal_weight=1, accessible_weight=1)
G.add_edge("Old Chem", "Bostock", normal_weight=1, accessible_weight=1)
G.add_edge("Bostock", "Perkins Library", normal_weight=1, accessible_weight=1)
G.add_edge("Bryan Center", "Penn", normal_weight=1, accessible_weight=1)
G.add_edge("Penn", "Wellness", normal_weight=1, accessible_weight=1)
G.add_edge("Wellness", "Wilson", normal_weight=4, accessible_weight=4)
G.add_edge("Wellness", "Gross Hall", normal_weight=4, accessible_weight=4)
G.add_edge("BioSci", "Gross Hall", normal_weight=3, accessible_weight=5)
G.add_edge("BioSci", "French", normal_weight=2)  # not accessible
G.add_edge("BioSci", "Physics", normal_weight=2, accessible_weight=2)
G.add_edge("French", "Physics", normal_weight=2, accessible_weight=2)
G.add_edge("Physics", "LSRC", normal_weight=3, accessible_weight=8)
G.add_edge("Physics", "Duke Chapel", normal_weight=3)  # not accessible
G.add_edge("Wilson", "West Union", normal_weight=7, accessible_weight=7)
G.add_edge("Gross Hall", "Bryan Center", normal_weight=4)  # not accessible
G.add_edge("Physics", "Bryan Center", normal_weight=3, accessible_weight=3)
G.add_edge("BioSci", "Bryan Center", normal_weight=3, accessible_weight=3)

#nodes
node_positions = {
    "Perkins Library": (1575, 515),
    "Duke Chapel": (1410, 425),
    "Bryan Center": (1170, 400),
    "West Union": (1250, 550),
    "Page": (1295, 460),
    "Allen": (1525, 700),
    "Social Sciences": (1700, 700),
    "Reuben Cooke": (1880, 700),
    "Old Chem": (1800, 550),
    "Bostock": (1835, 450),
    "Languages": (1695, 570),
    "Penn": (950, 370),
    "Wellness": (750, 370),
    "Wilson": (500, 735),
    "Gross Hall": (760, 215),
    "BioSci": (1090, 240),
    "French": (1150, 165),
    "Physics": (1240, 240),
    "LSRC": (1460, 175)
}

#find path (dfs)
def find_path(graph, start, end, accessible=False):
    if start not in graph.nodes or end not in graph.nodes:
        return None, float('inf')
    if start == end:
        return [start], 0

    weight_type = "accessible_weight" if accessible else "normal_weight"

    # subgraph w only valid edges for path type
    subgraph = nx.Graph()
    subgraph.add_nodes_from(graph.nodes(data=True))

    for u, v, d in graph.edges(data=True):
        if weight_type in d:
            subgraph.add_edge(u, v, weight=d[weight_type])

    try:
        path = nx.dijkstra_path(subgraph, start, end, weight="weight")
        length = nx.dijkstra_path_length(subgraph, start, end, weight="weight")
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')

#map visualization
def draw_graph(highlight_path=None):
    img = mpimg.imread("duke_map.png") 

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(img)
    ax.set_title("Duke Campus Map with Shortest Path", fontsize=14)
    ax.axis("off")

    #background graph
    nx.draw(G, pos=node_positions, ax=ax,
            node_color='white', node_size=100, edge_color='lightgray', width=1.5,
            with_labels=False)

    #highlight path
    if highlight_path and len(highlight_path) > 1:
        path_edges = list(zip(highlight_path, highlight_path[1:]))

        #highlight nodes
        nx.draw_networkx_nodes(G, node_positions, nodelist=highlight_path,
                               node_color='orange', node_size=250, ax=ax)

        nx.draw_networkx_labels(G, node_positions,
                                labels={n: n for n in highlight_path},
                                font_size=6, font_color='black', font_weight='bold', ax=ax,
                                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.1'))

        # highlight edges
        nx.draw_networkx_edges(G, node_positions, edgelist=path_edges,
                               width=3, edge_color='red', ax=ax)

    plt.tight_layout()
    plt.show()


#gui
def on_find_path():
    start = start_var.get()
    end = end_var.get()
    accessible = accessible_var.get()
    if not start or not end:
        messagebox.showerror("Error", "Please select both start and end locations.")
        return
    path, time = find_path(G, start, end, accessible)
    if path:
        result.set(f"{'Accessible' if accessible else 'Normal'} Path:\n{' -> '.join(path)}\n({time} min)")
        draw_graph(highlight_path=path)
    else:
        result.set("No path found.")

root = tk.Tk()
root.title("Duke Campus Map Path Finder")
root.geometry("400x300")

start_var = tk.StringVar()
end_var = tk.StringVar()
accessible_var = tk.BooleanVar()
result = tk.StringVar()

ttk.Label(root, text="Start Location:").pack(pady=5)
ttk.Combobox(root, textvariable=start_var, values=nodes, state="readonly").pack()

ttk.Label(root, text="End Location:").pack(pady=5)
ttk.Combobox(root, textvariable=end_var, values=nodes, state="readonly").pack()

ttk.Checkbutton(root, text="Accessible Route", variable=accessible_var).pack(pady=10)
ttk.Button(root, text="Find Path", command=on_find_path).pack()

ttk.Label(root, textvariable=result, wraplength=350, foreground="blue").pack(pady=15)

root.mainloop()