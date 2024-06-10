import click
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from logger import setup_logger
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import typing as tp
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import subprocess
import os
from dotenv import load_dotenv
import pickle

logger = setup_logger(__name__, 'train.log')
load_dotenv()


def dump_pickle(obj, filename: str) -> None:
    try:
        with open(filename, "wb") as f_out:
            pickle.dump(obj, f_out)
        logger.info(f"Successfully saved object to {filename}")
    except Exception as e:
        logger.error(f"Failed to save object to {filename}: {e}")


def setup_mlflow() -> None:
    try:
        subprocess.Popen(["mlflow", "ui", "--backend-store-uri", os.getenv("MLFLOW_TRACKING_URI")])
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        experiment = mlflow.get_experiment_by_name(os.getenv("MLFLOW_EXPERIMENT_NAME"))
        if experiment is None:
            mlflow.create_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))
        else:
            logger.info("Experiment already exists.")
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError) as e:
        logger.error(f"Error occurred while setting up MLflow: {e}")

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
    columns_to_drop = ['Loc_Name', 'Country_ID', 'Longitude', 'Latitude', 'Area']
    df = df.drop(columns_to_drop, axis=1)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols)
    return df_encoded


def split_data(df: pd.DataFrame, target_column: str) -> tp.Tuple:
    columns_to_drop = ['Loc_Name', 'Country_ID', 'Longitude', 'Latitude', 'Area']
    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    
    if len(existing_columns_to_drop) != len(columns_to_drop):
        missing_columns = set(columns_to_drop) - set(existing_columns_to_drop)
        logger.warning(f"Warning: Columns {missing_columns} not found in the DataFrame.")

    X = df.drop(existing_columns_to_drop + [target_column], axis=1)
    y = df[target_column]

    if y.dtype != 'int':
        unique_values = y.unique()
        logger.info(f"Unique values in the target variable {target_column} before conversion: {unique_values}")
        y = y.astype(int)
        logger.info(f"Converted target variable {target_column} to integers.")

    logger.info(f"Unique values in the target variable {target_column} after conversion: {y.unique()}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def train_and_save_model(model, model_name, X_train, y_train, X_test, y_test, output_path):
    with mlflow.start_run(run_name=f"{model_name} Classifier", nested=True):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc_score = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)

        mlflow.log_metric("Accuracy Score", acc_score)
        mlflow.log_text(class_report, f"{model_name} Classification Report")
        logger.info(f"Successfully logged {model_name} Model Metrics to mlflow.")

        # Save model
        model_path = os.path.join(output_path, f"{model_name.lower().replace(' ', '_')}_model.pkl")
        joblib.dump(model, model_path)
        logger.info(f"{model_name} Model saved to {model_path}")


@click.command()
@click.option(
    "--data_path",
    default="../Datasets/Bands.csv",
    help="Path where the dataset is saved"
)
@click.option(
    "--model_output_path",
    default="../Data/",
    help="Path where the model output should be saved"
)
def main(data_path: str, model_output_path: str) -> None:
    logger.info("Starting Training models...")
    df = read_data(data_path)
    df = impute_values(df)
    df_encoded = encode_values(df)

    X_train, X_test, y_train, y_test = split_data(df_encoded, target_column='Presence')
    dump_pickle((X_train, y_train), os.path.join(model_output_path, "train.pkl"))
    dump_pickle((X_test, y_test), os.path.join(model_output_path, "test.pkl"))

    with mlflow.start_run(run_name="model/geospatial_classifier_models"):
        mlflow.autolog(extra_tags={"developer": "@johnthuo"})
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("model_output_path", model_output_path)
        
        # Random Forest Classifier
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        train_and_save_model(rf_model, "Random Forest", X_train, y_train, X_test, y_test, model_output_path)
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)

        # Logistic Regression Classifier
        log_classifier = LogisticRegression(max_iter=1000, solver='lbfgs')
        train_and_save_model(log_classifier, "Logistic Regression", X_train, y_train, X_test, y_test, model_output_path)
        mlflow.log_param("max_iter", 1000)
        mlflow.log_param("solver", 'lbfgs')

if __name__ == "__main__":
    setup_mlflow()
    main()

# CMD -> python train.py --data_path ../Datasets/Bands.csv --model_output_path ../Data/