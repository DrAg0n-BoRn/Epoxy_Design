from ml_tools.optimization_tools import make_continuous_bounds_template
from ml_tools.schema import FeatureSchema
from paths import PM


if __name__ == "__main__":
    feature_schema = FeatureSchema.from_json(PM.engineering_artifacts)
    
    make_continuous_bounds_template(directory=PM.engineering_artifacts, feature_schema=feature_schema)
