import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display

# --- Data setup ---
bin_capacity = 10
items = [6, 5, 4, 3, 2, 5, 4, 6]
bins, states = [], []

# --- First Fit (recording step by step) ---
for item in items:
    placed = False
    for b in bins:
        if sum(b) + item <= bin_capacity:
            b.append(item)
            placed = True
            break
    if not placed:
        bins.append([item])
    states.append([list(b) for b in bins])  # save current state

# --- Compute statistics ---
total_bins = len(bins)
total_used = sum(sum(b) for b in bins)
total_capacity = total_bins * bin_capacity
wasted_space = total_capacity - total_used
efficiency = (total_used / total_capacity) * 100
avg_fill = total_used / total_bins

# --- Print statistics ---
print("📊 BIN PACKING STATISTICS")
print("---------------------------")
print(f"Total items: {len(items)}")
print(f"Bin capacity: {bin_capacity}")
print(f"Total bins used: {total_bins}")
print(f"Total used space: {total_used}")
print(f"Total wasted space: {wasted_space}")
print(f"Average fill per bin: {avg_fill:.2f}")
print(f"Packing efficiency: {efficiency:.2f}%")

# --- Visualization setup ---
fig, ax = plt.subplots(figsize=(5, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, (len(items) + 2) * (bin_capacity + 2))

def draw_state(state):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, (len(items) + 2) * (bin_capacity + 2))
    ax.set_title("Bin Packing Animation (First Fit)", fontsize=12)

    for i, b in enumerate(state):
        y = i * (bin_capacity + 2)
        ax.add_patch(patches.Rectangle((1, y), 6, bin_capacity,
                                       fill=False, edgecolor='black'))
        h = 0
        for item in b:
            ax.add_patch(patches.Rectangle((1, y + h), 6, item,
                                           color='skyblue', ec='black'))
            h += item
        ax.text(8.2, y + 3, f"Bin {i+1}\n{sum(b)}/{bin_capacity}", fontsize=8)

def update(frame):
    draw_state(states[frame])

ani = FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=False)

# --- Show animation in Colab ---
display(HTML(ani.to_jshtml()))

#@=====

# --- Save the animation ---
from matplotlib.animation import PillowWriter

# Save as MP4
ani.save("bin_packing_animation.mp4", writer='ffmpeg', fps=1)

# Save as GIF (alternative)
ani.save("bin_packing_animation.gif", writer=PillowWriter(fps=1))

print("✅ Animation saved as MP4 and GIF")
