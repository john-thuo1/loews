import click
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from logger import setup_logger
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
import typing as tp
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import os
from xgboost import XGBClassifier


# Setup logger for this module
logger = setup_logger(__name__, 'train.log')


def read_data(filename: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filename)
        logger.info(f"Successfully read data from {filename}")
        return df
    except FileNotFoundError:
        logger.error(f"The file {filename} does not exist.")
        raise
    except Exception as e:
        logger.error(f"Error reading {filename}: {e}")
        return None


def impute_values(df: pd.DataFrame) -> pd.DataFrame:
    if df.isna().sum().sum() == 0:
        logger.info("No missing values found in the dataset.")
        return df
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    
    if not categorical_cols.empty:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
        logger.info(f"Imputed missing categorical values in columns: {list(categorical_cols)}")
    
    if not numerical_cols.empty:
        num_imputer = SimpleImputer(strategy='mean')
        df[numerical_cols] = num_imputer.fit_transform(df[numerical_cols])
        logger.info(f"Imputed missing numerical values in columns: {list(numerical_cols)}")
    
    return df


def encode_values(df: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = df.select_dtypes(include=['object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols)
    return df_encoded


def split_data(df: pd.DataFrame, target_column: str) -> tp.Tuple:
    X = df.drop([target_column, 'Loc_Name', 'Country_ID', 'Longitude', 'Latitude', 'Area'], axis=1)
    y = df[target_column]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Log the shapes
    logger.info("X_train shape:", X_train.shape)
    logger.info("X_test shape:", X_test.shape)
    logger.info("y_train shape:", y_train.shape)
    logger.info("y_test shape:", y_test.shape)

    return X_train, X_test, y_train, y_test


def train_and_save_model(model, model_name, X_train, y_train, X_test, y_test, output_path):
    with mlflow.start_run(run_name=f"{model_name} Classifier", nested=True):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc_score = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)

        mlflow.log_metric("Accuracy Score", acc_score)
        mlflow.log_table(f"{model_name} Classification Report", class_report)
        logger.info(f"Successfully logged in {model_name} Model Metrics to mlflow.")

        # Save model
        model_path = os.path.join(output_path, f"{model_name.lower().replace(' ', '_')}_model.pkl")
        joblib.dump(model, model_path)
        logger.info(f"{model_name} Model saved to {model_path}")


@click.command()
@click.option(
    "--data_path",
    default="../Datasets/Bands.csv",
    help="Folder where Dataset is saved"
)
@click.option(
    "--model_output_path",
    default="../Data/Bands.csv",
    help="Folder where Dataset is saved"
)
def train_model(data_path: str, output_path: str) -> None:
    logger.info("Starting Training models...")
    df = read_data(data_path)
    df = impute_values(df)
    df_encoded = encode_values(df)

    X_train, X_test, y_train, y_test = split_data(df_encoded, target_column='Presence')

    with mlflow.start_run(run_name="model/geospatial_classifier_models"):
        mlflow.autolog(extra_tags={"developer": "@johnthuo"})
        mlflow.log_param("data-path", data_path)
        mlflow.log_param("model_output_path", output_path)
        
        # Random Forest Classifier
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        train_and_save_model(rf_model, "Random Forest", X_train, y_train, X_test, y_test, output_path)

        # Logistic Regression Classifier
        log_classifier = LogisticRegression(max_iter=1000, solver='lbfgs')
        train_and_save_model(log_classifier, "Logistic Regression", X_train, y_train, X_test, y_test, output_path)

        # xgboost Classifier
        xgb_model = XGBClassifier()
        train_and_save_model(xgb_model, "XGBoost", X_train, y_train, X_test, y_test, output_path)


if __name__ == "__main__":
    train_model()
