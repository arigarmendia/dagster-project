
from dagster_airbyte import load_assets_from_airbyte_instance, airbyte_assets
from rec_sys.resources import airbyte_resource



airbyte_connections = load_assets_from_airbyte_instance(airbyte_resource, key_prefix="recommmender_system_raw", connection_to_group_fn=lambda connection_name: "raw_data_ingestion")

