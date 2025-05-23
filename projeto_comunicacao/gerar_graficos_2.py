import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths and labels
base_path = "./"  # Change to your path
wifi_files = [
    "wifi-1500n-1m.csv", "wifi-1500n-10m.csv",
    "wifi-1500n-25m.csv", "wifi-1500n-50m.csv",
    "wifi-1500n-75m.csv", "wifi-1500n-100m.csv",
    "wifi-1500n-150m.csv", "wifi-1500n-200m.csv"

]
lora_files = [
    "lora-1500n-1m.csv", "lora-1500n-10m.csv",
    "lora-1500n-25m.csv", "lora-1500n-50m.csv",
    "lora-1500n-75m.csv", "lora-1500n-100m.csv",
    "lora-1500n-150m.csv", "lora-1500n-200m.csv"
]
distances = ["1m", "10m", "25m", "50m","75m", "100m", "150m", "200m"]

# Load datasets
wifi_data = {f.split('-')[-1].split('.')[0]: pd.read_csv(os.path.join(base_path, f)) for f in wifi_files}
lora_data = {f.split('-')[-1].split('.')[0]: pd.read_csv(os.path.join(base_path, f)) for f in lora_files}

# Prepare metrics
wifi_means, lora_means = [], []
wifi_speeds, lora_speeds = [], []
wifi_stddevs, lora_stddevs = [], []
wifi_losses, lora_losses = [], []

for dist in distances:
    wifi_df = wifi_data[dist]
    lora_df = lora_data[dist]

    # Mean delay
    wifi_means.append(wifi_df["Delta tempo"].mean())
    lora_means.append(lora_df["Delta tempo"].mean())

    # Speed
    wifi_speeds.append(wifi_df["Velocidade (m/s)"].mean())
    lora_speeds.append(lora_df["Velocidade (m/s)"].mean())

    # Delay std deviation
    wifi_stddevs.append(wifi_df["Delta tempo"].std())
    lora_stddevs.append(lora_df["Delta tempo"].std())

    # Packet loss (%)
    wifi_losses.append((wifi_df["Delta tempo"] == 0).sum() / len(wifi_df) * 100)
    lora_losses.append((lora_df["Delta tempo"] == 0).sum() / len(lora_df) * 100)

# Plotting
def plot_graph(y_wifi, y_lora, ylabel, title, filename):
    plt.figure()
    plt.plot(distances, y_wifi, marker='o', label='WiFi')
    plt.plot(distances, y_lora, marker='o', label='LoRa')
    plt.xlabel("Distance (m)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)

plot_graph(wifi_means, lora_means, "Average Delta Tempo (ns)", "Average Transmission Delay vs Distance", "Graph-avg-delay")
plot_graph(wifi_speeds, lora_speeds, "Speed (m/s)", "Average Speed vs Distance","graph-speed")
plot_graph(wifi_stddevs, lora_stddevs, "Standard Deviation of Delta Tempo (ns)", "Transmission Delay Variability","graph-variability")
plot_graph(wifi_losses, lora_losses, "Packet Loss (%)", "Packet Loss Percentage vs Distance", "graph-packets-lost")
