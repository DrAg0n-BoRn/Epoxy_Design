from ml_tools.optimization_tools import plot_optimal_feature_distributions
from paths import PM

if __name__ == "__main__":
    plot_optimal_feature_distributions(results_dir=PM["optimization results"])
