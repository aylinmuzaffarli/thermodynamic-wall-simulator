import math
import sys
import matplotlib.pyplot as plt
import numpy as np

print("=== THE THERMODYNAMIC WALL: SIMULATOR") 

workload_ops = input("Enter number of operations (N) [default: 1e15]: ")
N = float(workload_ops) if workload_ops.strip() else 1e15

temperature_k_env = input("Enter the temperature of environment (T in Kelvin) [default: 310]: ")
T = float(temperature_k_env) if temperature_k_env.strip() else 310.0

gap = input("Enter CMOS inefficiency  gap (G) [default: 1e7]: ")
G = float(gap) if gap.strip() else 1e7

serv_scale = input("Enter max number of servers in cluster [default: 10000]: ")
serv_scale = int(serv_scale) if serv_scale.strip() else 10000

cooling_input = input("Enter air-cooling power limit per node in Watts [default: 500]: ") 
cooling_limit_w = float(cooling_input) if cooling_input.strip() else 500.0

if N <= 0 or T <= 0 or G <= 0 or serv_scale <= 0 or cooling_limit_w <= 0:
    print("\n[ERROR]: All parameters (number operations, temperature of environment, inefficiency gap, number of servers, cooling limit) must be greater than 0!") 
    sys.exit(1)

K_B = 1.380649e-23
E_min = N * K_B * T * math.log(2)

E_actual = E_min * G

joules_per_kwh = 3.6e6

E_min_kwh = E_min / joules_per_kwh
E_actual_kwh = E_actual / joules_per_kwh

time_seconds = 1.0
total_power_watts = E_actual / time_seconds

power_per_server_watts = total_power_watts / serv_scale

is_cooling_wall_breached = power_per_server_watts > cooling_limit_w

operations_range = np.logspace(10, math.log10(N), 300)

e_min_curve = operations_range * K_B * T * math.log(2)
e_actual_curve = e_min_curve * G

plt.figure(figsize=(9, 6))

plt.plot(operations_range, e_min_curve, label="Landauer Limit (Theoretical Minimum)", color = "royalblue", linewidth = 2.5)
plt.plot(operations_range, e_actual_curve, label="Actual Silicon Energy (with Gap G)", color="crimson", linestyle="--", linewidth=2.5)

plt.xlabel("Number of Operations (N)", fontsize=12)
plt.ylabel("Energy (Joules)", fontsize=12)
plt.yscale("log") 
plt.xscale("log") 
plt.title("The Thermodynamic Wall: Theory vs Reality (Gap Analysis)", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, which="both", linestyle="--", alpha=0.6)

plt.savefig("landauer_vs_actual.png", dpi=300, bbox_inches="tight")
print("[+] Graph successfully saved as 'landauer_vs_actual.png' in your project folder!")

plt.show()

servers_axis = np.linspace(1, serv_scale, 400)

power_per_server_curve = total_power_watts / servers_axis

plt.figure(figsize=(9, 6))

plt.plot(servers_axis, power_per_server_curve, label="Heat Dissipation per Server", color="darkorange", linewidth=2.5)

plt.axhline(y=cooling_limit_w, color="red", linestyle=":", linewidth=2, label=f"Air-Cooling Limit ({cooling_limit_w}W per node)")

critical_servers = total_power_watts / cooling_limit_w

if 1 <= critical_servers <= serv_scale:
    plt.axvline(
        x=critical_servers, 
        color="purple", 
        linestyle="--", 
        linewidth=1.5, 
        label=f"Thermal Wall (~{int(critical_servers)} servers)"
    )

    plt.scatter(
    critical_servers,
    cooling_limit_w,
    color="purple",
    s=65,
    zorder=5,
    label="Critical Cooling Point"
    )
else:
    print("[!] Critical cooling point is outside the plotted server range.")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Cluster Scale (Number of Servers)", fontsize=12)
plt.ylabel("Power per Node (Watts)", fontsize=12)
plt.title("The Thermal Wall: Air-Cooling Limit vs. Cluster Scaling", fontsize=14, fontweight="bold")
plt.legend(fontsize=11, loc="upper right")
plt.grid(True, linestyle="--", alpha=0.6)

plt.xlim(1, serv_scale)

plt.savefig("thermal_wall.png", dpi=300, bbox_inches="tight")
print("[+] Graph successfully saved as 'thermal_wall.png' in your project folder!")

plt.show()

print("\n" + "="*60)
print("       THE THERMODYNAMIC WALL: SIMULATION RESULTS")
print("="*60)
print(f"[*] Workload Operations (N):         {N:.2e}")
print(f"[*] Environment Temperature (T):     {T:.2f} K")
print(f"[*] CMOS Inefficiency Gap (G):       {G:.2e}")
print(f"[*] Max Cluster Servers Scale:       {serv_scale}")
print(f"[*] Air-Cooling Limit per Node:      {cooling_limit_w:.1f} W")
print("-"*60)
print(f"[+] Landauer Minimum Energy (E_min): {E_min:.4e} J  ({E_min_kwh:.6f} kWh)")
print(f"[+] Actual Silicon Energy (E_actual):{E_actual:.4e} J  ({E_actual_kwh:.6f} kWh)")
print(f"[+] Total Cluster Power (t = 1s):    {total_power_watts:.2e} W")
print(f"[+] Critical Servers for Thermal Wall: {critical_servers:.1f}")
print("-"*60)

if is_cooling_wall_breached:
    print("[!] STATUS: THERMODYNAMIC WALL BREACHED AT THIS SCALE!")
    print(f"    To stay under {cooling_limit_w}W per node, you need at least")
    print(f"    {math.ceil(critical_servers)} servers for this workload.")
else:
    print("[STATUS: SAFE] Cluster operates within air-cooling limits at max scale.")

print("="*60 + "\n")