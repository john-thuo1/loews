import os
from typing import Type
import numpy as np
import pickle
import click
import mlflow
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from logger import setup_logger
from dotenv import load_dotenv
import joblib
import warnings


warnings.filterwarnings("ignore")

# Setup logger for this module
logger = setup_logger(__name__, 'optimize.log')
load_dotenv()


MODEL_CLASS_MAP = {
    'RandomForest': RandomForestClassifier,
    'LogisticRegression': LogisticRegression
}


def load_pickle(filename: str) -> any:
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def register_best_model(client: MlflowClient, top_n: int) -> str:
    logger.info("Registering best model...")
    experiment = client.get_experiment_by_name(os.getenv("MLFLOW_EXPERIMENT_NAME"))
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.accuracy DESC"]
    )

    best_run = runs[0]
    best_model_uri = f"runs:/{best_run.info.run_id}/model"
    mlflow.register_model(model_uri=best_model_uri, name="Best GeoSpatial Classifier Model")

    logger.info(f"Registered model {best_model_uri} as 'Best GeoSpatial Classifier Model'")
    return best_model_uri


def optimize_model(model_name: str, model_class: Type, search_space: dict, X_train, y_train, X_test, y_test, num_trials: int) -> None:
 def objective(params):
    model = model_class(**params)
    
    with mlflow.start_run(run_name=f'{model_name} Optimization', nested=True):
        mlflow.log_params(params)
        try:
            # Make a copy of input arrays to avoid modifying them
            X_train_copy = X_train.copy()
            y_train_copy = y_train.copy()
            model.fit(X_train_copy, y_train_copy)
        except Exception as e:
            logger.error(f"Error occurred during model fitting: {e}")
            raise e
        y_pred = model.predict(X_test)
        acc_optimized = accuracy_score(y_test, y_pred)
        mlflow.log_metric("Accuracy", acc_optimized)
        mlflow.sklearn.log_model(model, "model")

        return {'Accuracy': acc_optimized, 'status': STATUS_OK}


    with mlflow.start_run(run_name=f"GeoSpatial Models Optimization - {model_name}"):
        fmin(
            fn=objective,
            space=search_space,
            algo=tpe.suggest,
            max_evals=num_trials,
            trials=Trials(),
            rstate=np.random.default_rng(42)
        )
        
@click.command()
@click.option(
    "--data_path",
    default="../Data",
    type=str,
    help="Folder where Train & Test data was saved"
)
@click.option(
    "--num_trials",
    default=5,
    type=int,
    help="The number of parameter evaluations for the optimizer to explore"
)
@click.option(
    "--top_n",
    default=2,
    type=int,
    help="Number of top models that need to be evaluated to decide which one to promote"
)
def main(data_path: str, num_trials: int, top_n: int) -> None:
    logger.info("Starting model optimization...")
    client = MlflowClient()

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))


    model_optimizations = [
        {
            'model_name': 'RandomForest',
            'model_class': RandomForestClassifier,
            'search_space': {
                'n_estimators': scope.int(hp.quniform('n_estimators', 10, 1000, 1)),
                'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
                'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 10, 1)),
                'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 10, 1)),
                'max_features': hp.choice('max_features', ['auto', 'sqrt', 'log2', None]),
                'random_state': 42
            }
        },
        {
            'model_name': 'LogisticRegression',
            'model_class': LogisticRegression,
            'search_space': {
                'C': hp.loguniform('C', np.log(0.001), np.log(1000)),
                'solver': hp.choice('solver', ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']),
                'max_iter': scope.int(hp.quniform('max_iter', 100, 1000, 1)),
                'random_state': 42
            }
        }
    ]

    for model_opt in model_optimizations:
        optimize_model(
            model_name=model_opt['model_name'],
            model_class=model_opt['model_class'],
            search_space=model_opt['search_space'],
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            num_trials=num_trials
        )

    # Register the best model and retrieve its URI
    best_model_uri = register_best_model(client, top_n)
    best_model = mlflow.sklearn.load_model(best_model_uri)

    # Save the best model locally
    joblib.dump(best_model, os.path.join(data_path, "best_model.joblib"))    
    logger.info("Optimization completed successfully.")

if __name__ == "__main__":
    main()


# CMD -> 
