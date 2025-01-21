
from pathlib import Path
import os
import yaml
from dagster import Definitions, check, define_asset_job, AssetSelection, ScheduleDefinition, load_assets_from_modules, fs_io_manager, AssetKey, materialize, file_relative_path, ConfigMapping, RunConfig
#from rec_sys.assets.airbyte_assets import get_airbyte_assets
#from dagster_airbyte import load_assets_from_airbyte_instance
from dagster_mlflow import mlflow_tracking
#from dagster_dbt import dbt_assets
from rec_sys.assets import dbt, train_model
from rec_sys.assets.train_model import MyModelConfig
from rec_sys.resources import dbt_resource, postgres_io_manager, mlflow_resource # import the dbt resource
from rec_sys.assets.airbyte import airbyte_assets
#from rec_sys.configs import job_training_config



#print (f'Esta config recibe: {job_training_config}')

# Load dbt assets
dbt_assets = load_assets_from_modules(modules=[dbt], group_name="raw_data_transformation") # Load the assets from the file


# Load all training data assets
training_data_assets = load_assets_from_modules(modules=[train_model])

# Job to sync all resources
sync_all = define_asset_job("sync_all", selection="*")

# Load the YAML configuration
config_file_path = file_relative_path(__file__, "job_training_config.yml")
with open(config_file_path, "r") as file:
    job_training_config = yaml.safe_load(file)


model_job = define_asset_job(
    "model_training", ["model_trained"]
    )


# Asset definitions
defs = Definitions(
    assets=[airbyte_assets, *dbt_assets, *training_data_assets],
    jobs=[model_job, sync_all],
    #jobs=[model_job],
    resources={
        "dbt": dbt_resource,
        "postgres_io_manager": postgres_io_manager.configured({
            "connection_string": "env:POSTGRES_CONNECTION_STRING",
            "schema": "target"}),
        "default_io_manager": fs_io_manager,
        "mlflow": mlflow_tracking.configured({"experiment_name": "recommender_system"}),
    },
    schedules=[
        ScheduleDefinition(
            name="sync_all_assets_daily",
            job=sync_all,
            cron_schedule="@daily",
        ),
        ScheduleDefinition(
            name="model_job_hourly",
            job=model_job,
            cron_schedule="@hourly",
            run_config=RunConfig(
                ops={
                    "model_trained": MyModelConfig(
                        batch_size=128,
                        epochs=15,
                        learning_rate= 1e-3,
                        embeddings_dim=5,
                    )
                }
            ).to_config_dict()

        )
    ]
    
)

