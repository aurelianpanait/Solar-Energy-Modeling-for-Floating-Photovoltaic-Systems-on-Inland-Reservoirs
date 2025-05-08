import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Constants
PI = math.pi
SOLAR_CONSTANT = 1.353  # kW/m²

# Conversion functions
def deg_to_rad(theta):
    return theta * (2 * PI) / 360

def rad_to_deg(theta):
    return theta * 360 / (2 * PI)

# Load lake data
lake_files = {
    'LakeBicaz': 'LaculBicaz.csv',
    'LakeCerna': 'LaculCerna.csv',
    'LakeCincis': 'LaculCincis.csv',
    'LakeGuraApelor': 'LaculGuraApelor.csv',
    'LakePaltinu': 'LaculPaltinu.csv',
    'LakeSiriu': 'LaculSiriu.csv',
    'LakeStancaCostesti': 'LaculStancaCostesti.csv',
    'LakeSurduc': 'LaculSurduc.csv',
    'LakeVidraru': 'LaculVidraru.csv'
}

# Read and format data
def load_lake_data(filepath):
    df = pd.read_csv(filepath)
    data = []
    for i in range(len(df)):
        data.extend([
            df['Days'][i],
            df['Longitude'][i],
            df['Latitude'][i],
            df['Tilt'][i],
            df['DNI'][i],
            df['GHI'][i]
        ])
    return data

# Irradiance calculation function
def compute_irradiance(data):
    results = []
    for i in range(0, len(data), 6):
        day = data[i]
        longitude = data[i + 1]
        latitude = data[i + 2]
        tilt = data[i + 3]
        dni = data[i + 4]
        ghi = data[i + 5]

        decl = 23.45 * math.sin(deg_to_rad(360 * (284 + day) / 365))
        h_s = rad_to_deg(math.acos(-1 * math.tan(deg_to_rad(latitude)) * math.tan(deg_to_rad(decl))))

        H0 = ((SOLAR_CONSTANT / PI) * 24) * (1 + 0.033 * math.cos(deg_to_rad(360 * day) / 365)) * (
            math.cos(deg_to_rad(latitude)) * math.cos(deg_to_rad(decl)) * math.sin(deg_to_rad(h_s)) +
            (deg_to_rad(h_s) * math.sin(deg_to_rad(latitude)) * math.sin(deg_to_rad(decl)))
        )

        kt = dni / H0
        hd = ghi * ((0.775 + 0.00653 * (h_s - 90)) -
                    (0.505 + 0.00455 * (h_s - 90)) * math.cos(deg_to_rad(115 * kt - 103)))
        hb = ghi - hd
        hr = ghi * 0.5  # assumed reflectivity

        rb = ((math.sin(deg_to_rad(latitude - tilt)) * math.sin(deg_to_rad(decl))) +
              math.cos(deg_to_rad(latitude - tilt)) * math.cos(deg_to_rad(decl)) * math.cos(deg_to_rad(longitude))) / (
              math.sin(deg_to_rad(latitude)) * math.sin(deg_to_rad(decl)) +
              math.cos(deg_to_rad(latitude)) * math.cos(deg_to_rad(longitude)) * math.cos(deg_to_rad(decl)))

        rd = (1 + math.cos(deg_to_rad(tilt))) / 2
        rr = (1 - math.cos(deg_to_rad(tilt))) / 2

        ht = hr * rr + hb * rb + hd * rd
        results.append(ht)
    return results

# Monthly analysis and optimization
def calculate_monthly_irradiance(lake_name, data):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    irradiance_by_month = {month: [] for month in months}
    tilt_by_month = {month: [] for month in months}
    results_by_month = {month: [] for month in months}
    max_irradiance = {month: (0, 0) for month in months}

    for tilt_angle in range(90):
        for i in range(0, len(data), 6):
            data[i + 3] = tilt_angle  # set tilt
        results = compute_irradiance(data)
        for i, month in enumerate(months):
            irradiance_by_month[month].append(results[i])
            tilt_by_month[month].append(tilt_angle)
            results_by_month[month].append(results[i])

    for month in months:
        max_value = max(irradiance_by_month[month])
        max_index = irradiance_by_month[month].index(max_value)
        max_irradiance[month] = (tilt_by_month[month][max_index], max_value)

    return results_by_month, max_irradiance

# Plotting and printing results
def plot_monthly_results(lake_name, results_by_month, max_irradiance):
    months = list(results_by_month.keys())
    plt.figure(figsize=(18, 10))
    for i, month in enumerate(months):
        plt.subplot(4, 3, i + 1)
        plt.plot(range(90), results_by_month[month])
        plt.xlabel('Tilt angle (degrees)')
        plt.ylabel('Tilted Irradiance (kWh/m²)')
        plt.title(month)
        plt.tight_layout()
        angle, value = max_irradiance[month]
        print(f"The maximum value of tilted solar irradiance on {lake_name} for {month} occurs at a tilt angle of {angle}° with irradiance {round(value, 2)} kWh/m²")
    plt.show()

# Example usage (replace with your actual file paths)
# lake_name = 'LakeStancaCostesti'
# lake_data = load_lake_data('/path/to/LaculStancaCostesti.csv')
# results, max_vals = calculate_monthly_irradiance(lake_name, lake_data)
# plot_monthly_results(lake_name, results, max_vals)