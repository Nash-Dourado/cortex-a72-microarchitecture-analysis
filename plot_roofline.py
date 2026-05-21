import matplotlib.pyplot as plt
import numpy as np

# --- 1. Define the Hardware Limits (The Roof) ---
PEAK_GFLOPS = 48.0
PEAK_BANDWIDTH = 5.44
RIDGE_POINT = PEAK_GFLOPS / PEAK_BANDWIDTH

# --- 2. Define the Workload (The Dot) ---
WORKLOAD_I = 1.89
WORKLOAD_P = 2.18

# --- 3. Generate X-axis data (Arithmetic Intensity) ---
# We use a logarithmic space from 0.1 to 100 FLOPs/byte
x = np.logspace(-1, 2, 500)

# --- 4. Calculate the Roofline Y-values ---
# Attainable performance is the minimum of the memory limit and compute limit
y_memory_bound = x * PEAK_BANDWIDTH
y_compute_bound = np.full_like(x, PEAK_GFLOPS)
y_roof = np.minimum(y_memory_bound, y_compute_bound)

# --- 5. Create the Plot ---
plt.figure(figsize=(10, 6), dpi=150)

# Plot the primary Roofline envelope
plt.plot(x, y_roof, linewidth=3, color='#00A3A6', label='Cortex-A72 Hardware Limit')

# Plot the specific Workload Point
plt.scatter(WORKLOAD_I, WORKLOAD_P, color='#E84926', s=100, zorder=5, label='Naive MatMul Workload')

# Add subtle dashed lines connecting the point to the axes
plt.vlines(WORKLOAD_I, 0.1, WORKLOAD_P, linestyle='--', color='gray', alpha=0.5)
plt.hlines(WORKLOAD_P, 0.1, WORKLOAD_I, linestyle='--', color='gray', alpha=0.5)

# --- 6. Formatting the Graph ---
# A log-log scale is the industry standard for Roofline models
plt.xscale('log')
plt.yscale('log')

# Axis limits to keep the graph centered and clean
plt.xlim(0.1, 100)
plt.ylim(0.1, 100)

# Labels and Titles
plt.title('Roofline Performance Model: ARM Cortex-A72 (Raspberry Pi 4)', fontsize=14, pad=15)
plt.xlabel('Arithmetic Intensity (FLOPs/byte)', fontsize=12)
plt.ylabel('Performance (GFLOPS)', fontsize=12)

# Add Text Annotations directly onto the graph
plt.annotate(f'Peak Compute:\n{PEAK_GFLOPS} GFLOPS', xy=(20, 55), fontsize=10, color='black')
plt.annotate(f'Bandwidth Limit:\n{PEAK_BANDWIDTH} GB/s', xy=(0.2, 1.5), fontsize=10, color='black', rotation=40)

# Annotate the Ridge Point
plt.annotate(f'Ridge Point:\n{RIDGE_POINT:.2f} FLOPs/byte', 
             xy=(RIDGE_POINT, PEAK_GFLOPS), 
             xytext=(RIDGE_POINT*0.4, PEAK_GFLOPS*0.3),
             arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=10)

# Annotate the Workload Point
plt.annotate(f'Workload:\n({WORKLOAD_I} I, {WORKLOAD_P} GFLOPS)', 
             xy=(WORKLOAD_I, WORKLOAD_P), 
             xytext=(WORKLOAD_I*1.3, WORKLOAD_P*0.4),
             arrowprops=dict(facecolor='#E84926', arrowstyle='->'), color='#E84926', fontsize=10)

# Apply Grid and Legend
plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend(loc='lower right')

# --- 7. Save and Display ---
plt.tight_layout()
plt.savefig('roofline_cortex_a72.png')
print("Graph saved successfully as 'roofline_cortex_a72.png'")
plt.show()