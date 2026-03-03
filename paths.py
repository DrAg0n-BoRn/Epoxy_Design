from ml_tools.path_manager import DragonPathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = DragonPathManager(
    anchor_file=__file__,
    base_directories=["helpers", "results", "clean_data", "backups"]
)

# 2. Define directories and files.
### Base files
PM.clean_data_file = PM.clean_data / "clean_data.csv"

### Datasets
PM.datasets = PM.results / "Datasets"
PM.processed_data_file = PM.datasets / "processed_data.csv"
PM.final_data_file = PM.datasets / "predicted_samples.csv"

### Feature Engineering
PM.engineering = PM.results / "Feature Engineering"
PM.engineering_artifacts = PM.engineering / "Engineering Artifacts"
PM.engineering_plots = PM.engineering / "Engineering Plots"
PM.engineering_data_file = PM.datasets / "engineered_data.csv"

### MICE - VIF
PM.mice = PM.results / "MICE"
PM.mice_datasets = PM.mice / "MICE Datasets"
PM.mice_metrics = PM.mice / "MICE Metrics"
PM.vif = PM.results / "VIF"
PM.imputed_data_file = PM.datasets / "imputed_data.csv"

### Classification
PM.classification = PM.results / "Classification"
PM.classification_epoxy = PM.classification / "Epoxy"
PM.classification_filler = PM.classification / "Filler"
PM.classification_curing = PM.classification / "Curing"

### Regression Chain
PM.chain = PM.results / "Regression Chain"
PM.chain_temp = PM.chain / "temp"
# step1
PM.chain_tensile_file = PM.chain_temp / "tensile_strength.csv"
PM.chain_tensile = PM.chain / "Tensile Strength"
# step2
PM.chain_artifacts2 = PM.chain_temp / "artifacts step2"
PM.chain_flexural_file = PM.chain_temp / "flexural_strength.csv"
PM.chain_flexural = PM.chain / "Flexural Strength"

### Optimization
PM.optimization = PM.results / "Optimization"


# 3. Make directories and check status
PM.make_dirs()

if __name__ == "__main__":
    PM.status()
