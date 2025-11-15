import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display
import math

# ===========================================================
# 1. Greedy Spanner WITH Debugging (prints each accepted edge)
# ===========================================================

def greedy_spanner_with_states_debug(G, t=2):
    H = nx.Graph()
    H.add_nodes_from(G.nodes())

    # Deterministic sorting: first by weight, then by u, then v
    edges_sorted = sorted(G.edges(data=True),
                          key=lambda x: (x[2]['weight'], x[0], x[1]))

    states = [] 
    accepted_edges = []

    print("\n===== BEGIN GREEDY SPANNER DEBUG LOG =====\n")

    for step, (u, v, data) in enumerate(edges_sorted, start=1):
        w = data['weight']

        # shortest path distance in current H
        try:
            dist = nx.shortest_path_length(H, u, v, weight='weight')
        except nx.NetworkXNoPath:
            dist = math.inf

        # Rule: add only if dist > t * w
        if dist > t * w:
            H.add_edge(u, v, weight=w)
            accepted_edges.append((u, v))
            action = "ADD "
        else:
            action = "SKIP"

        print(f"STEP {step:2d}: {action}  edge=({u},{v})   dist={dist}   2*w={t*w}   edges_now={H.number_of_edges()}")

        # Save current state
        states.append(H.copy())

    print("\n===== FINAL RESULT =====")
    print("Accepted edges (in order):", accepted_edges)
    print("Final edge count:", H.number_of_edges())
    print("Final edges:", sorted(H.edges()))
    print("==========================================\n")

    return H, states


# ===========================================
# 2. Build Complete Graph K8 and Run Spanner
# ===========================================

G = nx.complete_graph(8)

# Give all edges weight = 1
for u, v in G.edges():
    G[u][v]['weight'] = 1

# Run greedy spanner
H, states = greedy_spanner_with_states_debug(G, t=2)


# ===========================================
# 3. Node positions for visualization
# ===========================================

pos = nx.spring_layout(G, seed=42)


# ===========================================
# 4. Animation
# ===========================================

fig, ax = plt.subplots(figsize=(6, 6))

def draw_frame(i):
    ax.clear()
    ax.set_title(f"Greedy Spanner Construction – Step {i+1}", fontsize=13)

    # Draw full graph (gray)
    nx.draw_networkx_nodes(G, pos, node_color="lightgray", ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", ax=ax)

    # Draw current spanner edges (blue)
    current_edges = states[i].edges()
    nx.draw_networkx_edges(
        G, pos,
        edgelist=list(current_edges),
        width=3,
        edge_color="blue",
        ax=ax
    )

    ax.text(
        0.5, -0.08,
        f"Blue edges = spanner edges at step {i+1} (count={states[i].number_of_edges()})",
        transform=ax.transAxes,
        ha='center',
        fontsize=10
    )

ani = FuncAnimation(fig, draw_frame, frames=len(states), interval=900, repeat=False)

display(HTML(ani.to_jshtml()))


# ===========================================
# 5. Final Statistics
# ===========================================

print("📊 GREEDY SPANNER STATISTICS")
print("-----------------------------")
print("Original edges:", G.number_of_edges())
print("Spanner edges:", H.number_of_edges())
print("Reduction:", 100 * (1 - H.number_of_edges() / G.number_of_edges()), "%")
print("Connected:", nx.is_connected(H))


# OPTIONAL: Save animation
from matplotlib.animation import PillowWriter

ani.save("greedy_spanner_K8.mp4", writer="ffmpeg", fps=1)
ani.save("greedy_spanner_K8.gif", writer=PillowWriter(fps=1))
print("\n🎬 Animation saved as MP4 and GIF.")
