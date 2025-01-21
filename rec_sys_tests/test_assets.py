import pytest
from dagster import check
from rec_sys.configs import job_training_config  # Adjust the import path if needed

def validate_job_config(job_config):
    """Validates the job configuration for required structure and keys."""
    # Ensure 'ops' contains 'model_trained'
    check.invariant(
        "model_trained" in job_config["ops"],
        "model_trained config is missing from job_training_config['ops']!"
    )
    # Ensure 'model_trained' contains required keys
    required_keys = {"batch_size", "epochs", "learning_rate", "embeddings_dim"}
    missing_keys = required_keys - job_config["ops"]["model_trained"]["config"].keys()
    check.invariant(
        not missing_keys,
        f"Missing keys in 'model_trained' config: {missing_keys}"
    )

def test_job_training_config():
    """Tests the job_training_config for correctness."""
    try:
        validate_job_config(job_training_config)
    except Exception as e:
        pytest.fail(f"Job training config validation failed: {e}")

