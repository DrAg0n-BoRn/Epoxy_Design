from ml_tools.PSO_optimization import multiple_objective_functions_from_dir, run_pso
from ml_tools.optimization_tools import plot_optimal_feature_distributions, parse_lower_upper_bounds
from ml_tools.utilities import deserialize_object 
from paths import PM
from helpers.constants import CONTINUOUS_RANGE


def main():
    binary_columns: list[str] = deserialize_object(filepath=PM["binary columns"]) # type: ignore
    
    objective_funcs, _ = multiple_objective_functions_from_dir(directory=PM["optimization models"],
                                                               add_noise=False,
                                                               task="maximization",
                                                               binary_features=len(binary_columns))
    
    lower_b, upper_b = parse_lower_upper_bounds(CONTINUOUS_RANGE)
    
    for obj_func in objective_funcs:
        run_pso(lower_boundaries=lower_b, 
                upper_boundaries=upper_b,
                objective_function=obj_func,
                save_results_dir=PM["optimization results"],
                save_format="both",
                swarm_size=200,
                max_iterations=3000,
                post_hoc_analysis=30)
    
    
def plot():
    plot_optimal_feature_distributions(results_dir=PM["optimization results"],
                                       save_dir=PM["optimization results"])


if __name__ == "__main__":
    main()
    plot()