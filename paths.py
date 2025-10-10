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
    "feature engineering": PM["data"] / "Feature Engineering",
    "feature engineering metrics": PM["results"] / "Feature Engineering Metrics",
    "mice datasets": PM["data"] / "MICE Datasets",
    "mice metrics": PM["results"] / "MICE Metrics",
    "vif datasets": PM["data"] / "VIF Datasets",
    "vif metrics": PM["results"] / "VIF Metrics",
    "train datasets": PM["data"] / "Train Datasets",
    "train metrics": PM["results"] / "Train Metrics",
    "optimization engineering": PM["data"] / "Optimization Engineering",
    "optimization engineering metrics": PM["results"] / "Optimization Engineering Metrics",
    "optimization train metrics": PM["results"] / "Optimization Train Metrics",
    "optimization results": PM["results"] / "Optimization Results",
})

# 2.2 📁 Subdirectories
PM.update({
    "feature engineering clip": PM["feature engineering"] / "Feature Engineering Clip",
    "feature engineering unclip": PM["feature engineering"] / "Feature Engineering Unclip",
})

# 2.3 📄 Files
PM.update({
    "clean data": PM["data"] / "clean_data.csv",
    "processed data": PM["data"] / "processed_data.csv",
    "engineered data unclip": PM["feature engineering unclip"] / "engineered_data_unclip.csv",
    "engineered data clip": PM["feature engineering clip"] / "engineered_data_clip.csv",
    "binary columns": PM["feature engineering"] / "BINARY_COLUMNS_list.joblib",
    "continuous columns": PM["feature engineering"] / "CONTINUOUS_COLUMNS_list.joblib",
    "optimization binary columns": PM["optimization engineering"] / "BINARY_COLUMNS_list.joblib",
    "optimization continuous columns": PM["optimization engineering"] / "CONTINUOUS_COLUMNS_list.joblib",
})

# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
