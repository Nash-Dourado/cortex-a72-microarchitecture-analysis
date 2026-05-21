import matplotlib.pyplot as plt
import pandas as pd
import io

# 1. Embedded Raw Data (Allows instant running in online compilers or local IDEs)
raw_telemetry_data = """Timestamp(s),Temperature(C),Frequency(MHz)
0.0,35.54,900
1.0,35.54,600
2.0,34.56,600
3.0,35.05,600
4.0,34.56,600
5.0,38.46,1800
6.0,39.92,1800
7.0,39.43,1800
8.0,41.38,1800
9.0,41.87,1800
10.0,42.84,1800
11.0,43.82,1800
12.0,43.33,1800
13.0,45.76,1800
14.0,44.30,1800
15.0,44.79,1800
16.0,44.79,1800
17.0,46.25,1800
18.0,45.76,1800
19.0,46.25,1800
20.0,45.76,1800
21.0,46.74,1800
22.0,45.76,1800
23.0,47.23,1800
24.0,46.25,1800
25.0,46.25,1800
26.0,47.71,1800
27.0,47.71,1800
28.0,47.71,1800
29.0,48.20,1800
30.0,48.20,1800
31.0,48.20,1800
32.0,48.20,1800
33.0,48.69,1800
34.0,48.69,1800
35.0,48.69,1800
36.0,51.12,1800
37.0,50.63,1800
38.0,50.15,1800
39.0,50.15,1800
40.0,50.63,1800
41.0,50.63,1800
42.0,49.66,1800
43.0,50.63,1800
44.0,51.61,1800
45.0,51.12,1800
46.0,51.12,1800
47.0,52.09,1800
48.0,52.09,1800
49.0,51.61,1800
50.0,51.61,1800
51.0,52.58,1800
52.0,52.58,1800
53.0,52.58,1800
54.0,52.09,1800
55.0,53.07,1800
56.0,51.61,1800
57.0,52.58,1800
58.0,53.07,1800
59.0,53.07,1800
60.0,53.56,1800
61.0,54.53,1800
62.0,53.07,1800
63.0,55.50,1800
64.0,52.58,1800
65.0,52.58,1800
66.0,50.63,1800
67.0,49.66,1800
68.0,48.69,1800
69.0,47.71,1800
70.0,48.20,600
71.0,47.71,600
72.0,46.74,600
73.0,46.74,600
74.0,46.74,600
75.0,46.74,600
76.0,45.76,600
77.0,45.76,600
78.0,45.76,600
79.0,45.76,600
80.0,45.28,600
81.0,45.76,600
82.0,44.30,600
83.0,45.76,600
84.0,45.76,600
85.0,44.79,600
86.0,45.28,600
87.0,43.82,600
88.0,44.30,600
89.0,46.25,600"""

# Read the string data into a pandas DataFrame
data = pd.read_csv(io.StringIO(raw_telemetry_data))
data.columns = data.columns.str.strip()

# 2. Initialize the plot layout
fig, ax1 = plt.subplots(figsize=(11, 6), dpi=150)

# 3. Plot Temperature on the Primary Y-Axis (Left)
color_temp = '#D32F2F'  # Deep Red
ax1.set_xlabel('Elapsed Time (seconds)', fontsize=12, labelpad=10)
ax1.set_ylabel('Core Temperature (°C)', color=color_temp, fontsize=12)

line_temp = ax1.plot(data['Timestamp(s)'], data['Temperature(C)'], 
                     color=color_temp, linewidth=2.5, label='Core Temperature (°C)')
ax1.tick_params(axis='y', labelcolor=color_temp)
ax1.set_ylim(30, 60)  # Perfectly scales your 34°C - 55.5°C tracking window

# 4. Plot Frequency on the Secondary Y-Axis (Right)
ax2 = ax1.twinx()  
color_freq = '#007A78'  # Arm Teal
ax2.set_ylabel('Core Clock Frequency (MHz)', color=color_freq, fontsize=12)

# Step plot to show discrete CPU frequency state adjustments
line_freq = ax2.step(data['Timestamp(s)'], data['Frequency(MHz)'], 
                     color=color_freq, linewidth=2, where='post', label='Clock Frequency (MHz)')
ax2.tick_params(axis='y', labelcolor=color_freq)
ax2.set_ylim(400, 2000)

# 5. Highlight the Active Workload Envelope (5.0s to 69.0s)
ax1.axvspan(5.0, 69.0, color='gray', alpha=0.12, label='Workload Active (sysbench)')

# 6. Formatting & Structural Layout Elements
plt.title('ARM Cortex-A72 Thermal Profile & DVFS Governor Response', fontsize=14, pad=15, fontweight='bold')
ax1.grid(True, which='both', linestyle='--', alpha=0.4)

# Consolidate both legends into a unified, clean box
lines = line_temp + line_freq
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# Custom contextual annotation highlighting the Governor downscale trigger at 70s
ax1.annotate('Workload Concluded:\nLinux CPUFreq Governor downscales\nfrequency to preserve idle power.', 
             xy=(70.0, 48.2), xytext=(35, 34),
             arrowprops=dict(facecolor='black', arrowstyle='->', lw=1),
             fontsize=10, bbox=dict(boxstyle="round,pad=0.5", fc="white", edgecolor="gray", alpha=0.9))

# 7. Layout Optimization and File Output
plt.tight_layout()
plt.savefig('thermal_dvfs_profile.png')
print("Telemetry chart generated successfully as 'thermal_dvfs_profile.png'!")
plt.show()