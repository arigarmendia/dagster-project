
from dagster_airbyte import load_assets_from_airbyte_instance
from ..resources import airbyte_resource



airbyte_assets = load_assets_from_airbyte_instance(airbyte_resource, key_prefix="recommmender_system_raw")