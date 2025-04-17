import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser

#create edges
G = nx.Graph()
nodes = ["Perkins Library", "Duke Chapel", "Bryan Center", "West Union", "Page", "Allen", 
         "Social Sciences", "Reuben Cooke", "Old Chem", "Bostock", "Languages", "Penn", 
         "Wellness", "Wilson", "Gross Hall", "BioSci", "French", "Physics", "LSRC"]
G.add_nodes_from(nodes)

G.add_edge("West Union", "Page", default_weight=1)  # not accessible
G.add_edge("West Union", "Perkins Library", default_weight=2, accessible_weight=2)
G.add_edge("Perkins Library", "Duke Chapel", default_weight=1, accessible_weight=2)
G.add_edge("Page", "Duke Chapel", default_weight=1, accessible_weight=1)
G.add_edge("West Union", "Allen", default_weight=2, accessible_weight=2)
G.add_edge("Page", "Bryan Center", default_weight=2)  # not accessible
G.add_edge("West Union", "Bryan Center", default_weight=1, accessible_weight=1)
G.add_edge("Duke Chapel", "Bryan Center", default_weight=2, accessible_weight=4)
G.add_edge("Perkins Library", "Languages", default_weight=1, accessible_weight=1)
G.add_edge("Perkins Library", "Allen", default_weight=1, accessible_weight=1)
G.add_edge("Perkins Library", "Social Sciences", default_weight=1, accessible_weight=1)
G.add_edge("Allen", "Social Sciences", default_weight=1, accessible_weight=1)
G.add_edge("Social Sciences", "Reuben Cooke", default_weight=1, accessible_weight=1)
G.add_edge("Languages", "Old Chem", default_weight=1, accessible_weight=1)
G.add_edge("Languages", "Social Sciences", default_weight=1, accessible_weight=1)
G.add_edge("Reuben Cooke", "Old Chem", default_weight=1, accessible_weight=1)
G.add_edge("Old Chem", "Bostock", default_weight=1, accessible_weight=1)
G.add_edge("Bostock", "Perkins Library", default_weight=1, accessible_weight=1)
G.add_edge("Bryan Center", "Penn", default_weight=1, accessible_weight=1)
G.add_edge("Penn", "Wellness", default_weight=1, accessible_weight=1)
G.add_edge("Wellness", "Wilson", default_weight=4, accessible_weight=4)
G.add_edge("Wellness", "Gross Hall", default_weight=4, accessible_weight=4)
G.add_edge("BioSci", "Gross Hall", default_weight=3, accessible_weight=5)
G.add_edge("BioSci", "French", default_weight=2)  # not accessible
G.add_edge("BioSci", "Physics", default_weight=2, accessible_weight=2)
G.add_edge("French", "Physics", default_weight=2, accessible_weight=2)
G.add_edge("Physics", "LSRC", default_weight=3, accessible_weight=8)
G.add_edge("Physics", "Duke Chapel", default_weight=3)  # not accessible
G.add_edge("Wilson", "West Union", default_weight=7, accessible_weight=7)
G.add_edge("Gross Hall", "Bryan Center", default_weight=4)  # not accessible
G.add_edge("Physics", "Bryan Center", default_weight=4, accessible_weight=4)
G.add_edge("BioSci", "Bryan Center", default_weight=3, accessible_weight=3)

#nodes
#node_positions = {
#    "Perkins Library": (1575, 515),
#    "Duke Chapel": (1410, 425),
#    "Bryan Center": (1170, 400),
#    "Brodhead Center": (1250, 550),
#}


node_positions = {
    "Social Sciences": (36.00176696782578, -78.93747970055111),
	"Old Chem": (36.00286152405447, -78.9377500885152),
	"Bostock": (36.002929267595746, -78.93837160220919),
	"Languages": (36.00225493310811, -78.93804097798417),
	"Penn": (36.00013715087822, -78.94080791683703),
	"Wellness": (35.99972870405351, -78.94125970403643),
	"Wilson": (35.99723376012868, -78.94100735092454),
    "French": (36.00307041734834, -78.94341767317096),
    "Physics": (36.00333833198901, -78.94253000899681),
    "Gross Hall": (36.00133946557715, -78.94475781060652),
    "LSRC": (36.00449510522876, -78.94196642519233),
    "BioSci": (36.00219492164742, -78.94305261083066),
    "Perkins Library": (36.00184747329267, -78.93856614647872),
	"Duke Chapel": (36.00195241128331, -78.94029518851522),
	"Bryan Center": (36.00091421047573, -78.9407338456745),
	"West Union": (36.00077963338793, -78.93936323823499),
	"Page": (36.00129135336987, -78.93992262979393),
	"Allen": (36.00128888402019, -78.93778809614771),
	"Reuben Cooke": (36.002446998795385, -78.93706961044322)
}

#find path (dfs)
def find_path(graph, start, end, accessible=False):
    if start not in graph.nodes or end not in graph.nodes:
        return None, float('inf')
    if start == end:
        return [start], 0

    weight_type = "accessible_weight" if accessible else "default_weight"

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
            node_color='#f7a8dc', node_size=100, edge_color='lightgray', width=1.5,
            with_labels=False)

    #highlight path
    if highlight_path and len(highlight_path) > 1:
        path_edges = list(zip(highlight_path, highlight_path[1:]))

        #highlight nodes
        nx.draw_networkx_nodes(G, node_positions, nodelist=highlight_path,
                               node_color='#f213a4', node_size=250, ax=ax)

        nx.draw_networkx_labels(G, node_positions,
                                labels={n: n for n in highlight_path},
                                font_size=6, font_color='black', font_weight='bold', ax=ax,
                                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

        # highlight edges
        nx.draw_networkx_edges(G, node_positions, edgelist=path_edges,
                               width=3, edge_color='#f213a4', ax=ax)

    plt.tight_layout()
    plt.show()


def draw_folium_map(paths=None, accessible=False, time=None):
    if not paths:
        return

    start_node = paths[0][1][0]
    campus_map = folium.Map(location=node_positions[start_node], zoom_start=17)

    #start = node_positions[highlight_path[0]]
    #campus_map = folium.Map(location=start, zoom_start=17)

    for name, coord in node_positions.items():
        folium.Marker(coord, tooltip=name).add_to(campus_map)


    color_map = {
        "Default": "red",
        "Accessible": "blue",
        "Same": "#c084fc"
    }

    for path_type, path, time in paths:
        coords = [node_positions[node] for node in path]

        # If times are a tuple (default_time, accessible_time)
        if isinstance(time, tuple):
            default_time, accessible_time = time
            label = f"Default & Accessible Path (Same): {path[0]} → {path[-1]} (Default: {round(default_time)} min, Accessible: {round(accessible_time)} min)"
        else:
            label = f"{path_type} Path: {path[0]} → {path[-1]} ({round(time)} min)"

        folium.PolyLine(
            coords,
            color=color_map.get(path_type, "gray"),
            weight=5,
            tooltip=label
        ).add_to(campus_map)
    """
    if highlight_path:
        coords = [node_positions[node] for node in highlight_path]
        #folium.PolyLine(coords, color="red", weight=5).add_to(campus_map)

        # Create label
        path_type = "Accessible" if accessible else "Default"
        path_label = f"{path_type} Path: {highlight_path[0]} → {highlight_path[-1]} ({time} min)"

        folium.PolyLine(
            coords,
            color="red",
            weight=5,
            tooltip=path_label  # This adds the hover label
        ).add_to(campus_map)
    """

    map_path = "duke_path_map.html"

    legend_html = """
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; 
        width: 200px;
        z-index: 9999; 
        font-size: 14px;
        background-color: rgba(255, 255, 255, 0.8);  /* Semi-transparent white */
        border-radius: 5px;  /* Rounded corners */
        box-shadow: 0 1px 5px rgba(0,0,0,0.4);  /* Subtle shadow */
        padding: 12px;
        ">
        <b>Path Legend</b><br>
        <div style="margin-top: 8px;">
            <span style="color:red; font-size: 16px;">&#9632;</span> Default Route<br>
            <span style="color:blue; font-size: 16px;">&#9632;</span> Accessible Route<br>
            <span style="color:#c084fc; font-size: 16px;">&#9632;</span> Same Path (Default + Accessible)<br>
        </div>
    </div>
    """
    campus_map.get_root().html.add_child(folium.Element(legend_html))

    logo_html = """
    <div style="
        position: fixed; 
        top: 20px; right: 20px; 
        width: 80px; height: 80px;  /* Made the container larger */
        z-index: 9999;
        background-color: rgba(255, 255, 255, 0.8);  /* 80% opaque white */
        border-radius: 5px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.4);
        padding: 2px;  /* Reduced padding to allow icon to fill more space */
        display: flex;
        align-items: center;
        justify-content: center;
        ">
        <img src="duke_logo.png" style="width: 90%; height: 90%; object-fit: contain;">
    </div>
    """
    campus_map.get_root().html.add_child(folium.Element(logo_html))

    campus_map.save(map_path)
    chrome_path = "open -a /Applications/Google\\ Chrome.app %s"
    webbrowser.get(chrome_path).open(map_path)




#gui
def on_find_path():
    start = start_var.get()
    end = end_var.get()
    route_choice = route_option.get()

    #show_both = show_both_var.get()
    #accessible = accessible_var.get()

    if not start or not end:
        messagebox.showerror("Error", "Please select both start and end locations.")
        return
    
    # get both paths regardless of option selected
    default_path, default_time = find_path(G, start, end, accessible=False)
    accessible_path, accessible_time = find_path(G, start, end, accessible=True)
    
    if not default_path and not accessible_path:
        result.set("No path found.")
        return

    text = ""
    if route_choice == "both":
        paths_to_draw = []
        if default_path and accessible_path and default_path == accessible_path:
            label = f"Default & Accessible Path (Same):\n{' → '.join(default_path)}\n(Default: {round(default_time)} min, Accessible: {round(accessible_time)} min)"
            result.set(label)
            draw_folium_map(paths=[("Same", default_path, (default_time, accessible_time))])
            return  # exit early since we've already handled display
        else:
            if default_path:
                text += f"Default Path:\n{' → '.join(default_path)}\n({round(default_time)} min)\n\n"
                paths_to_draw.append(("Default", default_path, default_time))
            if accessible_path:
                text += f"Accessible Path:\n{' → '.join(accessible_path)}\n({round(accessible_time)} min)"
                paths_to_draw.append(("Accessible", accessible_path, accessible_time))

            draw_folium_map(paths=paths_to_draw)

    elif route_choice == "accessible" and accessible_path:
        text += f"Accessible Path:\n{' → '.join(accessible_path)}\n({round(accessible_time)} min)"
        draw_folium_map(paths=[("Accessible", accessible_path, accessible_time)])

    elif route_choice == "default" and default_path:
        text += f"Default Path:\n{' → '.join(default_path)}\n({round(default_time)} min)"
        draw_folium_map(paths=[("Default", default_path, default_time)])

    result.set(text.strip())

    #path, time = find_path(G, start, end, accessible)
    """
    if path:
        result.set(f"{'Accessible' if accessible else 'Default'} Path:\n{' -> '.join(path)}\n({time} min)")
        draw_folium_map(highlight_path=path, accessible=accessible, time=time)
    else:
        result.set("No path found.")
    """


root = tk.Tk()

root.title("Duke Campus Map Path Finder")
root.geometry("400x300")

from PIL import Image, ImageTk

# Load and resize the icon
try:
    # Load and resize the icon
    icon_img = Image.open("duke_logo.png").resize((64, 64))
    icon_tk = ImageTk.PhotoImage(icon_img)
    
    # Place it at the top of your GUI using pack
    icon_label = ttk.Label(root, image=icon_tk)
    icon_label.image = icon_tk  # keep reference!
    icon_label.pack(pady=(10, 5))
except Exception as e:
    print(f"Could not load icon: {e}")

start_var = tk.StringVar()
end_var = tk.StringVar()
accessible_var = tk.BooleanVar()
result = tk.StringVar()

# to show both paths
show_both_var = tk.BooleanVar()
route_option = tk.StringVar(value="default")  # default selection

#ttk.Checkbutton(root, text="Show Both Paths", variable=show_both_var).pack(pady=5)

ttk.Label(root, text="Start Location:").pack(pady=5)
ttk.Combobox(root, textvariable=start_var, values=nodes, state="readonly").pack()

ttk.Label(root, text="End Location:").pack(pady=5)
ttk.Combobox(root, textvariable=end_var, values=nodes, state="readonly").pack()

ttk.Label(root, text="Route Type:").pack(pady=(10, 0))
ttk.Radiobutton(root, text="Default Route", variable=route_option, value="default").pack()
ttk.Radiobutton(root, text="Accessible Route", variable=route_option, value="accessible").pack()
ttk.Radiobutton(root, text="Show Both Paths", variable=route_option, value="both").pack()

#ttk.Checkbutton(root, text="Accessible Route", variable=accessible_var).pack(pady=10)
ttk.Button(root, text="Find Path", command=on_find_path).pack()

ttk.Label(root, textvariable=result, wraplength=350, foreground="blue").pack(pady=15)

root.mainloop()