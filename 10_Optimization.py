from typing import Any

from paths import PM
from helpers.constants import OPTIMIZATION_CONTINUOUS_RANGE

from ml_tools.utilities import find_model_artifacts, deserialize_object
from ml_tools.keys import PytorchArtifactPathKeys
from ml_tools.ML_models import AttentionMLP
from ml_tools.ML_inference import PyTorchInferenceHandler
from ml_tools.ML_optimization import create_pytorch_problem, run_optimization
from ml_tools.optimization_tools import parse_lower_upper_bounds
from ml_tools.custom_logger import load_list_strings


# --- single model function ---
def single_model_optimization(artifacts_dict: dict[str,Any], number_generations: int, repetitions: int):
    # parse artifact dict
    model_architecture_path = artifacts_dict[PytorchArtifactPathKeys.ARCHITECTURE_PATH]
    model_weights_path = artifacts_dict[PytorchArtifactPathKeys.WEIGHTS_PATH]
    scaler_path = artifacts_dict[PytorchArtifactPathKeys.SCALER_PATH]
    feature_names_path = artifacts_dict[PytorchArtifactPathKeys.FEATURES_PATH]
    target_names_path = artifacts_dict[PytorchArtifactPathKeys.TARGETS_PATH]
    
    # Parse list of strings
    target_names_list = load_list_strings(text_file=target_names_path, verbose=False)
    feature_names_list = load_list_strings(text_file=feature_names_path, verbose=False)
    
    # Model architecture
    model = AttentionMLP.load(file_or_dir=model_architecture_path, verbose=True)

    # Define pytorch handler
    pytorch_handler = PyTorchInferenceHandler(model=model,
                                            state_dict=model_weights_path,
                                            task="regression",
                                            device="cuda:0",
                                            scaler=scaler_path)

    # Define problem and searcher
    torch_problem, torch_searcher_factory = create_pytorch_problem(inference_handler=pytorch_handler,
                                                                    bounds=LOWER_UPPER_TUPLE,
                                                                    binary_features=BINARY_FEATURES_NUMBER,
                                                                    task="max",
                                                                    algorithm="Genetic")
    
    # Run optimization
    run_optimization(problem=torch_problem,
                    searcher_factory=torch_searcher_factory,
                    num_generations=number_generations,
                    target_name=target_names_list[0],
                    binary_features=BINARY_FEATURES_NUMBER,
                    save_dir=PM["optimization results"],
                    save_format="both",
                    feature_names=feature_names_list,
                    repetitions=repetitions)


# --- Batch function ---
def batch_optimization():
    # NOTE: this function has strict format requirements
    artifacts_dict_list = find_model_artifacts(target_directory=PM["optimization train metrics"], load_scaler=True, verbose=False)
    
    for artifacts_dict in artifacts_dict_list:
        single_model_optimization(artifacts_dict=artifacts_dict, 
                                  number_generations=200,
                                  repetitions=25)


if __name__ == "__main__":
    # --- Global Variables ---
    global BINARY_FEATURES_NUMBER, LOWER_UPPER_TUPLE
    
    binary_features: list[str] = deserialize_object(filepath=PM["optimization binary columns"], verbose=False) # type: ignore
    BINARY_FEATURES_NUMBER = len(binary_features)
    
    # Bounds
    LOWER_UPPER_TUPLE = parse_lower_upper_bounds(source=OPTIMIZATION_CONTINUOUS_RANGE)
    
    batch_optimization()
