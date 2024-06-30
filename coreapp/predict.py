# import os
# import numpy as np
# import joblib
# import click
# import pandas as pd
# import pickle
# import typing as tp
# from dotenv import load_dotenv
# from logger import setup_logger  

# # Set up logger
# logger = setup_logger(__name__, 'predict.log')



# Load Data
    
# click commands for model path, new_data to predict, output_path to save the predictions done and updated data.

# Do preprocessing on the data, and do the predictions and download the data with the new predictions.
# Map the predictions on the data
    # @click.command()
    # @click.option(
    # "--model_path",
    # default="../Data/best_model.joblib",
    # type=str,
    # help="Path to the saved model file"
    # )
    # @click.option(
    # "--data_path",
    # default="../Data/new_data.pkl",
    # type=str,
    # help="Path to the new data file"
    # )
    # @click.option(
    # "--output_path",
    # default="../Data/predictions.pkl",
    # type=str,
    # help="Path to save the predictions"
    # )
    # def predict(model_path: str, data_path: str, output_path: str) -> pd.Dataframe: