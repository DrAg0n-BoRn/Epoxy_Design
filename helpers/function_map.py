import polars as pl
from .constants import TARGETS, RAW_TARGETS
from ml_tools.ETL_engineering import TransformationRecipe, KeywordDummifier, NumberExtractor, MultiNumberExtractor, RatioCalculator


TRANSFORMATION_RECIPE = TransformationRecipe()

##### "环氧": "epoxy"
# One-hot encode into predefined groups
epoxy_group_names = [
        "epoxy_bisphenol_A/F", 
        "epoxy_phenolic", 
        "epoxy_aliphatic_cycloaliphatic", 
        "epoxy_flexibly_modified", 
        "epoxy_special_structure"
    ]

epoxy_group_keywords = [
        ["E-5", "E5", "E-4", "E4", "DGEBA", "BADGE", "NPEL", "双酚 F", "双酚F", "E1NT", "二烯丙基双酚", "桐油基两", "桐油基三", "TED", "AG", "柚皮素环氧树脂", "BH140", "MFE"],
        ["酚醛"],
        ["TDE"],
        ["PUS", "柔性改性环氧树脂", "PDMS"],
        ["TGDDM", "DCPD", "HER", "噁唑烷酮改性环氧树脂", "自固化羧基功能化双酚", "桐油基环氧树脂", "环三膦腈"]
    ]

epoxy_transformer = KeywordDummifier(
    group_names = epoxy_group_names,
    group_keywords = epoxy_group_keywords
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧",
    output_col_names = epoxy_group_names,
    transform = epoxy_transformer
)

##### "分子量": "molecular weight"
# Extract the molecular weight from the column
molecular_weight_transformer = NumberExtractor(
    dtype = "float",
    round_digits = 2
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "分子量",
    output_col_names = "molecular_weight(g/mol)",
    transform = molecular_weight_transformer
)

##### "固化剂": "curing agent"
# One-hot encode into predefined groups
# TODO
curing_transformer = KeywordDummifier(
    group_names = [],
    group_keywords = [
        []
    ]
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "固化剂",
    output_col_names = curing_transformer.group_names,
    transform = curing_transformer
)

##### "环氧/固化剂配比": "epoxy/curing agent ratio"
# extract the ratio
ratio_epoxy_curing_transformer = RatioCalculator()

TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧/固化剂配比",
    output_col_names = "epoxy_curing_ratio",
    transform = ratio_epoxy_curing_transformer
)

##### "碳纤维含量": "carbon fiber content"
# Parse percentage values
carbon_fiber_transformer = NumberExtractor(
    dtype = "float",
    round_digits = 2
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "碳纤维含量",
    output_col_names = "carbon_fiber(%)",
    transform = carbon_fiber_transformer
)

##### "填料种类": "type of filler"
# # One-hot encode into predefined groups
# TODO
filler_transformer = KeywordDummifier(
    group_names = [],
    group_keywords = [
        []
    ]
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "填料种类",
    output_col_names = filler_transformer.group_names,
    transform = filler_transformer
)

##### "填料比例": "filler proportion"
# Custom transformer
def filler_proportion_transformer(col: pl.Series) -> pl.Series:
    """
    Parse ratios and percentages
    """
    parse_ratios = col.str.extract(r'(\d+\.?\d*\s?:\s?\d+\.?\d*)').to_list()
    
    cleaned_ratios = list()
    for result_string in parse_ratios:
        if result_string is None:
            cleaned_ratios.append(None)
        else:
            left, right = result_string.strip().split(":")
            left = round(float(left.strip()), 2)
            right = round(float(right.strip()), 2)
            if right == 0 and left == 0:
                cleaned_ratios.append(None)
            elif right == 0:
                cleaned_ratios.append(left)
            elif left == 0:
                cleaned_ratios.append(right)
            else:
                true_ratio = 100 * left / right
                cleaned_ratios.append(true_ratio)
    
    polars_ratios = pl.Series("ratios", cleaned_ratios)
    
    # parse numbers as fallback
    parse_numbers = col.str.extract(r"(\d+\.?\d*)").cast(pl.Float64, strict=False)
    
    polars_numbers_expr = (
        pl.when(parse_numbers.is_null()).then(None)
        # .when(parse_numbers < 1.0).then(parse_numbers * 100)
        # .when(parse_numbers < 10.0).then(parse_numbers * 10)
        .otherwise(parse_numbers)
        .round(2)
        .alias("numbers")
    )
    
    polars_numbers = pl.select(polars_numbers_expr).to_series()
    
    final_expr = (
        pl.when(polars_ratios.is_null()).then(polars_numbers)
        .otherwise(polars_ratios)
        .round(2)
        .alias("filler_proportion(%)")
    )
    
    # evaluate and return expression
    return pl.select(final_expr).to_series()


TRANSFORMATION_RECIPE.add(
    input_col_name = "填料比例",
    output_col_names = "filler_proportion(%)",
    transform = filler_proportion_transformer
)

##### "促进剂": "accelerator"
# # One-hot encode into predefined groups
# TODO
accelerator_transformer = KeywordDummifier(
    group_names = [],
    group_keywords = [
        []
    ]
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "促进剂",
    output_col_names = accelerator_transformer.group_names,
    transform = accelerator_transformer
)

##### "促进剂含量": "accelerator content"
# Parse percentage values
accelerator_content_transformer = NumberExtractor(
    dtype = "float",
    round_digits = 2
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "促进剂含量",
    output_col_names = "accelerator_content(%)",
    transform = accelerator_content_transformer
)

##### "温度": "temperature"
# Custom transformer
def temperature_transformer(col: pl.Series) -> pl.Series:
    """
    Extract the temperature and convert to Kelvin
    
    strange data: "室温", "常温"
    """
    parse_strings = col.str.extract(r'(\d+\.?\d*|温)', 1)

    temp_expr = (
        pl.when(parse_strings.is_null()).then(None)
        .when(parse_strings.str.contains("温")).then(26)
        .otherwise(parse_strings)
        .cast(pl.Float64, strict=False)
        .round(2)
        + 273.15
    ).alias("temperature(K)")
    
    # evaluate and return expression
    return pl.select(temp_expr).to_series()


TRANSFORMATION_RECIPE.add(
    input_col_name = "温度",
    output_col_names = "temperature(K)",
    transform = temperature_transformer
)


##### Targets
# All targets have a single value to extract
for raw_target, target in zip(RAW_TARGETS, TARGETS):
    current_target_transformer = NumberExtractor(
        dtype = "float",
        round_digits = 2
    )
    
    TRANSFORMATION_RECIPE.add(
        input_col_name = raw_target,
        output_col_names = target,
        transform = current_target_transformer
    )
