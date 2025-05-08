import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Set your coordinates here (example: a location in Romania)
latitude = "45.5"
longitude = "25.5"
tilt = 18  # Panel tilt angle (not used in this script but can be passed on)

# NASA POWER API parameters
params = {
    "parameters": "ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI",
    "community": "RE",
    "longitude": longitude,
    "latitude": latitude,
    "format": "JSON",
    "start": "20200101",
    "end": "20201231",
    "tempAverage": "DAILY",
    "time": "24"
}

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Make the API request
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    ghi_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    dni_data = data['properties']['parameter']['ALLSKY_SFC_SW_DNI']

    records = []
    for date_str in ghi_data:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        records.append({
            'Date': date_obj,
            'GHI': ghi_data[date_str],
            'DNI': dni_data.get(date_str, 'N/A')
        })

    # Create DataFrame and monthly averages
    df = pd.DataFrame(records)
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_avg = df.groupby('Month').mean().reset_index()

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg['Month'].astype(str), monthly_avg['GHI'], label='GHI')
    plt.plot(monthly_avg['Month'].astype(str), monthly_avg['DNI'], label='DNI')
    plt.xlabel('Month')
    plt.ylabel('Average Irradiance (kWh/m²)')
    plt.title('Monthly Average GHI and DNI')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    plt.savefig('outputs/import_cu_grafic.png')
    plt.show()

    # Export CSV (optional)
    monthly_avg.to_csv('outputs/nasa_monthly_irradiance.csv', index=False)

    print("✅ Monthly averages calculated and saved to outputs/.")
else:
    print("❌ Failed to fetch data:", response.status_code)
