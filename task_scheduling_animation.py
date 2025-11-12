import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display

# --- Example data ---
tasks = [4, 6, 3, 5, 2, 7, 4, 3]   # task durations
num_machines = 3                    # number of machines

# --- Scheduling using List Scheduling (Greedy) ---
machines = [[] for _ in range(num_machines)]
end_times = [0] * num_machines
states = []

for t in tasks:
    m = end_times.index(min(end_times))  # choose machine that gets free first
    machines[m].append((end_times[m], t))  # store (start_time, duration)
    end_times[m] += t
    # snapshot of current state
    state = [[(s, d) for (s, d) in mach] for mach in machines]
    states.append(state)

# --- Statistics ---
makespan = max(end_times)
avg_load = sum(tasks) / num_machines
efficiency = (sum(tasks) / (num_machines * makespan)) * 100

print("📊 SCHEDULING STATISTICS")
print("------------------------")
print(f"Total tasks: {len(tasks)}")
print(f"Machines: {num_machines}")
print(f"Makespan (total time): {makespan}")
print(f"Average load per machine: {avg_load:.2f}")
print(f"Scheduling efficiency: {efficiency:.2f}%")

# --- Visualization setup ---
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['skyblue', 'lightgreen', 'lightcoral', 'khaki', 'plum', 'orange']

def draw_state(state):
    ax.clear()
    ax.set_xlim(0, makespan + 2)
    ax.set_ylim(-1, num_machines)
    ax.set_title("Task Scheduling Visualization (List Scheduling)", fontsize=12)
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine ID")

    for m_id, mach in enumerate(state):
        for i, (start, dur) in enumerate(mach):
            ax.add_patch(patches.Rectangle((start, -m_id - 0.4), dur, 0.8,
                                           color=colors[i % len(colors)], ec='black'))
            ax.text(start + dur / 2, -m_id, f"T{i+1}", ha='center', va='center', fontsize=8)
        ax.text(-1.5, -m_id, f"M{m_id+1}", va='center', fontsize=9)

def update(frame):
    draw_state(states[frame])

ani = FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=False)
display(HTML(ani.to_jshtml()))

#@====@csquickrevisionshorts 

#--- Save the animation ---
from matplotlib.animation import PillowWriter

# Save as MP4
ani.save("task_scheduling_animation.mp4", writer='ffmpeg', fps=1)

# Save as GIF (alternative)
ani.save("task_scheduling_animation.gif", writer=PillowWriter(fps=1))

print("✅ Animation saved as MP4 and GIF")
