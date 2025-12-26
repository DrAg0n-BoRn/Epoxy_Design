from .constants import TARGET_tensile_strength, TARGET_flexural_strength, TARGET_elongation_at_break, TARGET_impact_strength
from ml_tools.ETL_engineering import DragonTransformRecipe, NumberExtractor, TriRatioCalculator, TemperatureExtractor, MultiNumberExtractor


TRANSFORMATION_RECIPE = DragonTransformRecipe()

##### "环氧": "epoxy" -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧",
    output_col_names = "Epoxy",
    transform = "rename"
)

# curing_transformer -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "固化剂",
    output_col_names = "Curing",
    transform = "rename"
)

##### "环氧/固化剂配比": "epoxy/curing agent ratio"
# extract the ratio epoxy/epoxy/curing
TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧/固化剂配比",
    output_col_names = ["Epoxy/Epoxy Ratio", "Epoxy/Curing Ratio"],
    transform = TriRatioCalculator(handle_zeros=True)
)

##### "填料种类": "type of filler" -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "填料种类",
    output_col_names = "Filler",
    transform = "rename"
)

##### "填料比例": "filler proportion"
# extract multiple proportions
TRANSFORMATION_RECIPE.add(
    input_col_name = "填料比例",
    output_col_names = ["Filler Proportion(%)", "Filler Proportion 2(%)", "Filler Proportion 3(%)"],
    transform = MultiNumberExtractor(num_outputs=3)
)

##### "温度": "temperature"
# Parse temperature and transform to K
TRANSFORMATION_RECIPE.add(
    input_col_name = "温度",
    output_col_names = "Temperature(K)",
    transform = TemperatureExtractor(convert="K")
)


###########################################################
##### Targets - All targets have a single value to extract
# Tensile Strength
TRANSFORMATION_RECIPE.add(
    input_col_name="拉伸强度",
    output_col_names=TARGET_tensile_strength,
    transform=NumberExtractor()
)

# Flexural strength
TRANSFORMATION_RECIPE.add(
    input_col_name="弯曲强度",
    output_col_names=TARGET_flexural_strength,
    transform=NumberExtractor()
)

# Elongation at break
TRANSFORMATION_RECIPE.add(
    input_col_name="断裂伸长率",
    output_col_names=TARGET_elongation_at_break,
    transform=NumberExtractor()
)

# Impact strength
TRANSFORMATION_RECIPE.add(
    input_col_name="冲击强度",
    output_col_names=TARGET_impact_strength,
    transform=NumberExtractor()
)
