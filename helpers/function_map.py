from ml_tools.ETL_engineering import DragonTransformRecipe, NumberExtractor, TriRatioCalculator, TemperatureExtractor, MultiNumberExtractor
from .constants import (TENSILE_STRENGTH,
                        FLEXURAL_STRENGTH,
                        ELONGATION_AT_BREAK,
                        IMPACT_STRENGTH,
                        EPOXY,
                        CURING,
                        FILLER,
                        EPOXY_EPOXY_RATIO,
                        EPOXY_CURING_RATIO,
                        FILLER_PROPORTION,
                        FILLER_PROPORTION_2,
                        FILLER_PROPORTION_3,
                        TEMPERATURE)


TRANSFORMATION_RECIPE = DragonTransformRecipe()

##### "环氧": "epoxy" -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧",
    output_col_names = EPOXY,
    transform = "rename"
)

# curing_transformer -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "固化剂",
    output_col_names = CURING,
    transform = "rename"
)

##### "环氧/固化剂配比": "epoxy/curing agent ratio"
# extract the ratio epoxy/epoxy/curing
TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧/固化剂配比",
    output_col_names = [EPOXY_EPOXY_RATIO, EPOXY_CURING_RATIO],
    transform = TriRatioCalculator(handle_zeros=True)
)

##### "填料种类": "type of filler" -> Categorical
# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "填料种类",
    output_col_names = FILLER,
    transform = "rename"
)

##### "填料比例": "filler proportion"
# extract multiple proportions
TRANSFORMATION_RECIPE.add(
    input_col_name = "填料比例",
    output_col_names = [FILLER_PROPORTION, FILLER_PROPORTION_2, FILLER_PROPORTION_3],
    transform = MultiNumberExtractor(num_outputs=3)
)

##### "温度": "temperature"
# Parse temperature and transform to K
TRANSFORMATION_RECIPE.add(
    input_col_name = "温度",
    output_col_names = TEMPERATURE,
    transform = TemperatureExtractor(convert="K")
)


###########################################################
##### Targets - All targets have a single value to extract
# Tensile Strength
TRANSFORMATION_RECIPE.add(
    input_col_name="拉伸强度",
    output_col_names=TENSILE_STRENGTH,
    transform=NumberExtractor()
)

# Flexural strength
TRANSFORMATION_RECIPE.add(
    input_col_name="弯曲强度",
    output_col_names=FLEXURAL_STRENGTH,
    transform=NumberExtractor()
)

# Elongation at break
# TRANSFORMATION_RECIPE.add(
#     input_col_name="断裂伸长率",
#     output_col_names=ELONGATION_AT_BREAK,
#     transform=NumberExtractor()
# )

# Impact strength
# TRANSFORMATION_RECIPE.add(
#     input_col_name="冲击强度",
#     output_col_names=IMPACT_STRENGTH,
#     transform=NumberExtractor()
# )
