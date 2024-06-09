from faker import Faker
import random
import pandas as pd
import typing as tp
import click
from logger import setup_logger

logger = setup_logger(__name__, 'generate_data.log')



def load_file(input_file_path: str) -> tp.List[str]:
    logger.info(f"Loading districts from file path: {input_file_path}")
    try:
        with open(input_file_path, 'r') as file:
            districts_list = [line.strip() for line in file if line]
        logger.debug(f"Loaded districts: {districts_list}")
        return districts_list
    except Exception as e:
        logger.error(f"Failed to load file {input_file_path}: {e}")
        raise

@click.command()
@click.option("--input_file_path", default='../Data/districts.txt', help="Text File containing List of Districts in Kenya")
@click.option("--num_rows", default=5000, help="Number of rows for dummy data")
@click.option("--output_file_path", default='../Datasets/data.csv', help="Output file path for the generated dummy data")
def generate_dummy_data(input_file_path: str, num_rows: int, output_file_path: str) -> None:
    logger.info("Starting the dummy data generation process")
    
    synth = Faker()

    # Load districts from the file
    try:
        districts_list = load_file(input_file_path)
    except Exception as e:
        logger.critical("Aborting dummy data generation due to an error in loading districts")
        return

    logger.info(f"Generating {num_rows} rows of dummy data")
    data = {
        'Report_Date': [synth.date_this_decade() for _ in range(num_rows)],
        'Location': [synth.random_element(districts_list) for _ in range(num_rows)],
        'Vegetation_Details': random.choices(
            ["Staple Crops", "Pasture and Grasslands", "Vegetable Crops", "Fruit Orchards", "Unknown"], k=num_rows),
        'Land_Size(Acres)': [random.uniform(0.5, 1000) for _ in range(num_rows)],
        'Season': random.choices(
            ["Wet Season/Long Rains(April-June)", "Short Rains/Wet Season(April-June)", "Dry/Hot Season(January-March)", 
             "Dry/Cold Season(July-August)", "Dry/Warm Season(September-October)", "Wet Season/Short Rains(November-December)"], 
            k=num_rows),
        'Species': random.choices(
            ["Unknown", "Bombay Locust ( Nomadacris succincta)", "Desert Locusts(Schistocerca gregaria)", "Grasshoppers", 
             "Migratory locust (Locusta migratoria)", "Red locust (Nomadacris septemfasciata)", "Spur Throated Locusts", 
             "Tree locust (Anacridium sp.)"], k=num_rows),
        'Stage': random.choices(
            ["Adults", "Hoppers/Nymph(Breeding Ground)", "Fledglings(Young Adults)", "Eggs(Breeding Ground)", "Unknown"], 
            k=num_rows),
        'Soil_Type': random.choices(
            ["Loose Sandy Soil", "Clay Soil", "Loam Soil", "Alluvial Soil", "Laterite Soil", "Peat Soil", "Unknown"], k=num_rows),
        'Distribution': random.choices(
            ["Entire Field", "Paddock Only", "Entire Area", "Unknown"], k=num_rows),
        'GPS_Coordinates': [(synth.latitude(), synth.longitude()) for _ in range(num_rows)],
    }

    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    try:
        df.to_csv(output_file_path, index=False)
        logger.info(f"Dummy data successfully saved to  file path {output_file_path}")
    except Exception as e:
        logger.error(f"Failed to save dummy data to file path {output_file_path}: {e}")

if __name__ == "__main__":
    generate_dummy_data()
