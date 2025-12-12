from ml_tools.path_manager import DragonPathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = DragonPathManager(
    anchor_file=__file__,
    base_directories=["helpers", "data", "results", "clean_data"]
)

# 2. Define directories and files. Available project-wide via PM.get().
# 2.1 📁 Directories
PM.logs = PM.ROOT / "logs"
PM.feature_engineering = PM.data / "Feature Engineering"
PM.mice_datasets = PM.data / "MICE Datasets"
PM.mice_metrics = PM.results / "MICE Metrics"
PM.vif_datasets = PM.data / "VIF Datasets"
PM.vif_metrics = PM.results / "VIF Metrics"
PM.train_metrics = PM.results / "Train Metrics"
PM.optimization_results = PM.results / "Optimization Results"

# 2.2 📁 Subdirectories
PM.engineering_datasets = PM.feature_engineering / "Datasets"
PM.engineering_artifacts = PM.feature_engineering / "Artifacts"


# 2.3 📄 Files
PM.clean_data_file = PM.clean_data / "clean_data.csv"
PM.processed_data_file = PM.data / "processed_data.csv"
PM.engineered_data_file = PM.feature_engineering_datasets / "engineered_data.csv"
PM.mice_dataset_file = PM.mice_datasets / "mice_dataset.csv"



# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
