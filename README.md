This code has been developed as part of a research study on floating photovoltaic (FPV) systems deployed on water reservoirs. The computational logic is derived from a peer-reviewed research paper ([Springer, 2021](https://link.springer.com/article/10.1007/s12517-021-06674-7), which originally provided a Perl implementation for calculating solar irradiation on tilted FPV surfaces. The model was translated into Python and significantly enhanced with new features to estimate maximum solar irradiance values across various tilt angles and water surfaces.

The datasets used as input consist of:
	•	CSV files exported from QGIS, containing the geographic coordinates (latitude, longitude) and reservoir-specific solar parameters (GHI – Global Horizontal Irradiance, DNI – Direct Normal Irradiance).
	•	JSON files retrieved from the NASA POWER API, which provided high-resolution daily solar data. This data was processed into monthly averages using Python’s pandas library, and plotted to visualize the seasonal variation of solar resource availability across different locations.

The core functionality of the code allows the user to select any lake from a predefined list and:
	•	simulate solar irradiance on tilted panels throughout the year,
	•	determine the optimal tilt angle for each month that maximizes the irradiance,
	•	and visualize the results using Matplotlib.

This tool supports spatial and temporal optimization for FPV deployment, offering a valuable decision-making aid for energy yield estimation and siting of floating solar systems.

🛰️ Data Sources
	•	NASA POWER API
Used to extract daily GHI (Global Horizontal Irradiance) and DNI (Direct Normal Irradiance) for each lake location. Data is aggregated into monthly averages.
	•	QGIS CSV exports
Used to provide latitude, longitude, and base inputs for each reservoir.

⚙️ Features
	•	Converts GHI to TGI (Tilted Global Irradiance) using solar geometry:
	•	Declination angle
	•	Hour angle
	•	Beam, diffuse, and reflected components
	•	Simulates irradiance at all tilt angles (0° to 89°)
	•	Visualizes irradiance evolution for each month using Matplotlib
	•	Identifies the optimal tilt angle per month with maximum energy potential
