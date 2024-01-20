from faker import Faker
import random
import pandas as pd

# Number of rows to generate
num_rows = 5000

# Read districts from file
with open('loews\districts.txt', 'r') as file:
    districts_list = [line.strip() for line in file if line]

# Initialize Faker
fake = Faker()

# Dummy data that will be visualized
data = {
    'Report_Date': [fake.date_this_decade() for _ in range(num_rows)],
    'Location': [fake.random_element(districts_list) for _ in range(num_rows)],
    'Vegetation_Details': random.choices(["Staple Crops", "Pasture and Grasslands", "Vegetable Crops", "Fruit Orchards", "Unknown"], k=num_rows),
    'Land_Size': random.choices(['< 1 Acre', '1 Acre', '2 Acres', '> 5 Acres', '1 Ha', '> 1 Ha', '> 10 Ha', '> 100 Ha'], k=num_rows),
    'Season': random.choices(["Wet Season/Long Rains(April-June)", "Short Rains/Wet Season(April-June)", "Dry/Hot Season(January-March)", "Dry/Cold Season(July-August)", "Dry/Warm Season(September-October)", "Wet Season/Short Rains(November-December)"], k=num_rows),
    'Species': random.choices(["Unknown", "Bombay Locust ( Nomadacris succincta)", "Desert Locusts(Schistocerca gregaria)", "Grasshoppers", "Migratory locust (Locusta migratoria)", "Red locust (Nomadacris septemfasciata)", "Spur Throated Locusts", "Tree locust (Anacridium sp.)"], k=num_rows),
    'Stage': random.choices(["Adults", "Hoppers/Nymph(Breeding Ground)", "Fledglings(Young Adults)", "Eggs(Breeding Ground)", "Unknown"], k=num_rows),
    'Soil_Type': random.choices(["Loose Sandy Soil", "Clay Soil", "Loam Soil", "Alluvial Soil", "Laterite Soil", "Peat Soil", "Unknown"], k=num_rows),
    'Distribution': random.choices(["Entire Field", "Paddock Only", "Entire Area", "Unknown"], k=num_rows),
    'GPS_Coordinates': [(fake.latitude(), fake.longitude()) for _ in range(num_rows)],
}

df = pd.DataFrame(data)
df.to_csv("loews\Datasets\data.csv")

print(df.head())
