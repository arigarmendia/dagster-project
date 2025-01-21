from dagster import execute_job, DagsterInstance
from rec_sys.definitions import model_job  # Import your model_job definition

# Create a Dagster instance
instance = DagsterInstance.local_temp()

# Execute the job with the specific asset names
result = execute_job(
    job=model_job,
    run_config={
        "ops": {
            "model_trained": {
                "config": {
                    "batch_size": 128,
                    "epochs": 10,
                    "learning_rate": 1e-3,
                    "embeddings_dim": 5,
                }
            }
        }
    },
    instance=instance,
)

assert result.success, "Dry-run test failed!"


