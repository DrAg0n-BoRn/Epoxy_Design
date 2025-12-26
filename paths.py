from ml_tools.path_manager import DragonPathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = DragonPathManager(
    anchor_file=__file__,
    base_directories=["helpers", "data", "results", "clean_data", "backups"]
)

# 2. Define directories and files. Available project-wide via PM.get().
# 2.1 📁 Directories
PM.logs = PM.ROOT / "logs"
PM.feature_engineering = PM.data / "Feature Engineering"
PM.mice_datasets = PM.data / "MICE Datasets"
PM.mice_metrics = PM.results / "MICE Metrics"
PM.vif = PM.data / "VIF"
PM.train_datasets = PM.data / "Train Datasets"
PM.train_metrics = PM.results / "Train Metrics"
PM.optimization_results = PM.results / "Optimization Results"

# 2.2 📁 Subdirectories
PM.engineering_datasets = PM.feature_engineering / "Datasets"
PM.engineering_artifacts = PM.feature_engineering / "Artifacts"
PM.engineering_plots = PM.feature_engineering / "Plots"
PM.engineering_artifacts_2 = PM.feature_engineering / "Artifacts 2"
PM.engineering_artifacts_3 = PM.feature_engineering / "Artifacts 3"

# Make chain-training subdirectories
PM.train_metrics_1 = PM.train_metrics / "Train Metrics 1"
PM.train_artifacts_1 = PM.train_metrics_1 / "Train Artifacts 1"
PM.train_checkpoints_1 = PM.train_metrics_1 / "Train Checkpoints 1"
PM.train_evaluation_1 = PM.train_metrics_1 / "Train Evaluation 1"

PM.train_metrics_2 = PM.train_metrics / "Train Metrics 2"
PM.train_artifacts_2 = PM.train_metrics_2 / "Train Artifacts 2"
PM.train_checkpoints_2 = PM.train_metrics_2 / "Train Checkpoints 2"
PM.train_evaluation_2 = PM.train_metrics_2 / "Train Evaluation 2"

PM.train_metrics_3 = PM.train_metrics / "Train Metrics 3"
PM.train_artifacts_3 = PM.train_metrics_3 / "Train Artifacts 3"
PM.train_checkpoints_3 = PM.train_metrics_3 / "Train Checkpoints 3"
PM.train_evaluation_3 = PM.train_metrics_3 / "Train Evaluation 3"

# 2.3 📄 Files
PM.clean_data_file = PM.clean_data / "clean_data.csv"
PM.processed_data_file = PM.data / "processed_data.csv"
PM.engineered_data_file = PM.engineering_datasets / "engineered_data.csv"
PM.step1_data_file = PM.train_datasets / "step1.csv"
PM.step2_data_file = PM.train_datasets / "step2.csv"
PM.step3_data_file = PM.train_datasets / "step3.csv"

# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
