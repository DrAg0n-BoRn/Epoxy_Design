from ml_tools.path_manager import PathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = PathManager(
    anchor_file=__file__,
    base_directories=["helpers", "data", "results"]
)

# 2. Define and register specific directories and files. Available project-wide via PM.get().
# 2.1 📁 Directories
PM.update({
    "logs": PM["ROOT"] / "Logs",
    "feature engineering metrics": PM["data"] / "Feature Engineering Metrics",
    "feature engineering clip": PM["data"] / "Feature Engineering Clip Datasets",
    "feature engineering unclip": PM["data"] / "Feature Engineering Unclip Datasets",
    "serialized objects": PM["data"] / "Serialized Objects",
})

# 2.2 📄 Files
PM.update({
    "raw data": PM["data"] / "epoxy_raw_data.csv",
    "processed data": PM["data"] / "processed_data.csv",
})

# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
