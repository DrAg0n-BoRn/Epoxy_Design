from ml_tools.path_manager import PathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = PathManager(
    anchor_file=__file__,
    base_directories=["helpers", "data", "results"]
)

# 2. Define directories and files. Available project-wide via PM.get().
# 2.1 📁 Directories
PM.update({
    "logs": PM["ROOT"] / "Logs",
    "serialized objects": PM["data"] / "Serialized Objects",
    "feature engineering metrics": PM["results"] / "Feature Engineering Metrics",
    "feature engineering clip": PM["data"] / "Feature Engineering Clip",
    "feature engineering unclip": PM["data"] / "Feature Engineering Unclip",
    "mice metrics": PM["results"] / "MICE Metrics",
    "mice datasets": PM["data"] / "MICE Datasets",
    "vif metrics": PM["results"] / "VIF Metrics",
    "vif datasets": PM["data"] / "VIF Datasets",
    "model metrics": PM["results"] / "Model Results",
    "model datasets": PM["data"] / "Train Datasets",
    "optimization models": PM["data"] / "Optimization Models",
    "optimization results": PM["results"] / "Optimization Results"
})

# 2.2 📄 Files
PM.update({
    "clean data": PM["data"] / "cleaned_data.csv",
    "processed data": PM["data"] / "processed_data.csv",
    "feature columns": PM["serialized objects"] / "FEATURE_COLUMNS_list.joblib",
    "binary columns": PM["serialized objects"] / "BINARY_COLUMNS_list.joblib",
    "feature names": PM["optimization models"] / "feature_names.txt",
    "model architecture": PM["optimization models"] / "architecture.json"
})

# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
