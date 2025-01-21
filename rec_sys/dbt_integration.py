# from pathlib import Path

from dagster_dbt import DbtProject


dbt_project = DbtProject(
    project_dir="/Users/ari/Desktop/github_repos/db_postgres",
)
# project_dir=Path(__file__).joinpath("..", "..", "db_postgres").resolve()

# print(project_dir)