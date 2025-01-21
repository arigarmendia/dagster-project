from dagster import EnvVar
from .resources import mlflow_resource

           
mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system'
        }            
    }
}


# job_training_config = {
#     "ops": {
#         "model_trained": {
#             "config": {
#                 "batch_size": 128,
#                 "epochs": 10,
#                 "learning_rate": 1e-3,
#                 #"embeddings_dim": 5,
#             }
#         }
#     },
#         "resources": {
#             "mlflow": mlflow_resource,
#     }
# }



