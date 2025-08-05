from pathlib import Path
from typing import Union

from paths import PM
from helpers.constants import CONTINUOUS_RANGE_OPTIMAL, NUMBER_BINARY_FEATURES

from ml_tools.path_manager import list_files_by_extension
from ml_tools.ML_models import MultilayerPerceptron, load_architecture
from ml_tools.ML_inference import PyTorchInferenceHandler
from ml_tools.ML_optimization import create_pytorch_problem, run_optimization
from ml_tools.optimization_tools import parse_lower_upper_bounds, plot_optimal_feature_distributions
from ml_tools.custom_logger import load_list_strings


# --- Global Variables ---
# Bounds
lower_upper_tuple = parse_lower_upper_bounds(source=CONTINUOUS_RANGE_OPTIMAL)
# feature names
feature_names = load_list_strings(text_file=PM["feature names"])

# --- single model function ---
def single_model_optimization(state_dict_path: Union[str,Path], target_name: str, number_generations: int, repetitions: int):
    # Model architecture
    model = load_architecture(filepath=PM["model architecture"], expected_model_class=MultilayerPerceptron, verbose=False)

    # Define pytorch handler
    pytorch_handler = PyTorchInferenceHandler(model=model,
                                            state_dict=state_dict_path,
                                            task="regression",
                                            device="mps")

    # Define problem and searcher
    torch_problem, torch_searcher_factory = create_pytorch_problem(inference_handler=pytorch_handler,
                                                                    bounds=lower_upper_tuple,
                                                                    binary_features=NUMBER_BINARY_FEATURES,
                                                                    task="max",
                                                                    algorithm="Genetic")
    
    # Run optimization
    run_optimization(problem=torch_problem,
                    searcher_factory=torch_searcher_factory,
                    num_generations=number_generations,
                    target_name=target_name,
                    binary_features=NUMBER_BINARY_FEATURES,
                    save_dir=PM["optimization results"],
                    save_format="both",
                    feature_names=feature_names,
                    repetitions=repetitions)


# --- Plot function ---
def plot():
    plot_optimal_feature_distributions(results_dir=PM["optimization results"])


# --- Batch function ---
def main():
    #RENAME state dictionary filenames to target names
    model_weights_dict = list_files_by_extension(directory=PM["optimization models"], extension="pth")
    
    for target_filename, fpath in model_weights_dict.items():
        single_model_optimization(state_dict_path=fpath,
            target_name=target_filename,
            number_generations=600,
            repetitions=25)


if __name__ == "__main__":
    #NOTE: RENAME state dictionary filenames to target names
    main()
    plot()
