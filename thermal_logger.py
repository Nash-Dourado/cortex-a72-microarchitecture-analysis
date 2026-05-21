import time

def get_hardware_state():
    temp_raw = open("/sys/class/thermal/thermal_zone0/temp").read()
    temp_c = float(temp_raw) / 1000.0

    freq_raw = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq").read()
    freq_mhz = float(freq_raw) / 1000.0

    return temp_c, freq_mhz

print("Timestamp(s),Temperature(C),Frequency(MHz)")
start_time = time.time()

try:
    while True:
        elapsed = time.time() - start_time
        temp, freq = get_hardware_state()
        print(f"{elapsed:.1f},{temp:.2f},{freq:.0f}", flush=True)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nLogging stopped.")