
from pathlib import Path
import os
import yaml
from dagster import Definitions, define_asset_job, AssetSelection, ScheduleDefinition, load_assets_from_modules, fs_io_manager, file_relative_path
#from rec_sys.assets.airbyte_assets import get_airbyte_assets
#from dagster_airbyte import load_assets_from_airbyte_instance
from dagster_mlflow import mlflow_tracking
#from dagster_dbt import dbt_assets
from rec_sys.assets import my_dbt, train_model
#from rec_sys.assets.train_model import MyModelConfig
from rec_sys.resources import dbt_resource, postgres_io_manager
from rec_sys.assets.airbyte import airbyte_connections


# --------------Load config parameters from config.yml file--------------------#

# Load the cofigs.yml file (config parameters file)
config_file_path = file_relative_path(__file__, "configs.yml")
with open(config_file_path, "r") as file:
    config_parameters = yaml.safe_load(file)

# -------------------------------Load assets-----------------------------------#

# Load dbt assets
dbt_assets = load_assets_from_modules(modules=[my_dbt], group_name="raw_data_transformation")

# Load all training data assets
training_data_assets = load_assets_from_modules(modules=[train_model])

# -------------------------------Define jobs-----------------------------------#

# Job to sync the Airbyte connections
airbyte_sync_job = define_asset_job("airbyte_sync_job" , selection=AssetSelection.groups("raw_data_ingestion"))

# Job to orchestrate dbt
dbt_sync_job = define_asset_job("dbt_sync_job" , selection=AssetSelection.groups("raw_data_transformation"))

data_prep_job = define_asset_job("data_prep_job", selection=AssetSelection.groups("data_preparation"))

# Job to train, eval and storte the model
model_job = define_asset_job(
    "model_training", ["model_trained","model_stored", "model_metrics"], # Just trying another way to select assets
    )

# Job to sync all resources
sync_all = define_asset_job("sync_all", selection="*")
    


# -------------------------------Definitions-----------------------------------#

defs = Definitions(
    assets=[airbyte_connections, *dbt_assets, *training_data_assets],
    jobs=[airbyte_sync_job, dbt_sync_job, data_prep_job, model_job, sync_all],
    resources={
        "dbt": dbt_resource,
        "postgres_io_manager": postgres_io_manager.configured({
            "connection_string": "env:POSTGRES_CONNECTION_STRING",
            "schema": "target"}),
        #"default_io_manager": fs_io_manager,
        "mlflow": mlflow_tracking.configured(config_parameters['mlflow']),
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
            run_config=config_parameters['model_job_hourly']
        )
    ]
    
)

