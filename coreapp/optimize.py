import os
import numpy as np
import pickle
import click
import mlflow
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from dotenv import load_dotenv
import joblib
import warnings
import typing as tp

from logger import setup_logger  

warnings.filterwarnings("ignore")


logger = setup_logger(__name__, 'optimize.log')
load_dotenv()


MODEL_CLASS_MAP = {
    'RandomForest': RandomForestClassifier,
}


def load_pickle(filename: str) -> tp.Any:
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

    X_train_copy = X_train.copy(deep=True)
    y_train_copy = y_train.copy(deep=True)
    X_test_copy = X_test.copy(deep=True)
    y_test_copy = y_test.copy(deep=True)

    def objective(params):
        model = RandomForestClassifier(**params)
        
        with mlflow.start_run(run_name='RandomForest Optimization', nested=True):
            mlflow.log_params(params)

            model.fit(X_train_copy, y_train_copy)
            y_pred = model.predict(X_test_copy)
            rf_optimized = accuracy_score(y_test_copy, y_pred)
            mlflow.log_metric("Accuracy", rf_optimized)
            mlflow.sklearn.log_model(model, "model")

            # Negate the Accuracy Score to work as the Loss as hyperopt only takes that.
            return {'loss': -rf_optimized, 'status': STATUS_OK}

    search_space = {
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 1000, 1)),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
        'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 10, 1)),
        'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 10, 1)),
        'max_features': hp.choice('max_features', ['sqrt', 'log2', None]),
        'random_state': 42     
    }

    with mlflow.start_run(run_name="Classifier Optimization"):
        fmin(
            fn=objective,
            space=search_space,
            algo=tpe.suggest,
            max_evals=num_trials,
            trials=Trials(),
            rstate=np.random.default_rng(42)
        )

        # Register the best model from Random Forest and retrieve its URI
        best_model_uri = register_best_model(client, top_n)
        best_model = mlflow.sklearn.load_model(best_model_uri)

        # Save the best model locally
        joblib.dump(best_model, os.path.join(data_path, "best_model.joblib"))
        logger.info("Optimization completed successfully.")

if __name__ == "__main__":
    main()

# CMD -> python optimize.py --data_path ../Data --num_trials 10 --top_n 5
