from .constants import TARGETS, RAW_TARGETS
from ml_tools.ETL_engineering import DragonTransformRecipe, KeywordDummifier, NumberExtractor, TriRatioCalculator, AutoDummifier, TemperatureExtractor


TRANSFORMATION_RECIPE = DragonTransformRecipe()

##### "环氧": "epoxy"
# One-hot encode into predefined groups
# epoxy_group_names = [
#         "epoxy_Bisphenol A/F", 
#         "epoxy_Phenolic", 
#         "epoxy_Aliphatic Cycloaliphatic", 
#         "epoxy_Flexibly Modified", 
#         "epoxy_Special Structure"
#     ]

# epoxy_group_keywords = [
#         ["E-5", "E5", "E-4", "E4", "DGEBA", "BADGE", "NPEL", "双酚 F", "双酚F", "E1NT", "二烯丙基双酚", "桐油基两", "桐油基三", "TED", "AG", "柚皮素环氧树脂", "BH140", "MFE"],
#         ["酚醛"],
#         ["TDE"],
#         ["PUS", "柔性改性环氧树脂", "PDMS"],
#         ["TGDDM", "DCPD", "HER", "噁唑烷酮改性环氧树脂", "自固化羧基功能化双酚", "桐油基环氧树脂", "环三膦腈"]
#     ]

# epoxy_transformer = KeywordDummifier(
#     group_names = epoxy_group_names,
#     group_keywords = epoxy_group_keywords
# )

# Rename
TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧",
    output_col_names = "Epoxy",
    transform = "rename"
)



##### "分子量": "molecular weight"
# Extract the molecular weight from the column
# molecular_weight_transformer = NumberExtractor(
#     dtype = "float",
#     round_digits = 2
# )

# TRANSFORMATION_RECIPE.add(
#     input_col_name = "分子量",
#     output_col_names = "Molecular Weight(g/mol)",
#     transform = molecular_weight_transformer
# )


##### "固化剂": "curing agent"
# One-hot encode into predefined groups
# curing_transformer = KeywordDummifier(
#     group_names = [
#         "curing_Aromatic Amines",
#         "curing_Aliphatic Amines",
#         "curing_Anhydrides",
#         "curing_Imidazoles",
#         "curing_Phenolic Resins",
#     ],
#     group_keywords = [
#         ["DDM", "PDA", "DDS", "ADPS", "二氨基二苯甲烷", "间苯二胺"],
#         ["二乙烯三胺", "D230", "D400", "DETDA", "三乙烯四胺", "DEAPA", "9035", "胺类固化剂"],
#         ["MTHPA", "HHPA", "MNA", "GA", "酸酐"],
#         ["咪唑"],
#         ["酚醛树脂"],
#     ]
# )

curing_transformer = AutoDummifier()

TRANSFORMATION_RECIPE.add(
    input_col_name = "固化剂",
    output_col_names = "Curing",
    transform = curing_transformer
)

##### "环氧/固化剂配比": "epoxy/curing agent ratio"
# extract the ratio
ratio_epoxy_curing_transformer = TriRatioCalculator(handle_zeros=True)

TRANSFORMATION_RECIPE.add(
    input_col_name = "环氧/固化剂配比",
    output_col_names = ["Epoxy/Epoxy Ratio", "Epoxy/Curing Ratio"],
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
    output_col_names = "Carbon Fiber(%)",
    transform = carbon_fiber_transformer
)

##### "填料种类": "type of filler"
# # One-hot encode into predefined groups
# filler_transformer = KeywordDummifier(
#     group_names = [
#         "filler_Toughening",
#         "filler_Thermal Conductive",
#         "filler_Flame Retardant",
#         "filler_Electric-conductive/Shielding",
#         "filler_Reinforcement"
#     ],
#     group_keywords = [
#         ["TBN", "PU", "纳米氧化铝", "竹纤维", "聚醚型聚氨酯预聚物", "PES", "改性竹长纤维", "AFV", "环氧基聚硅氧烷", "端羧基丁腈橡胶"],
#         ["BN", "Al"],
#         ["FR", "DOPO", "APP", "磷腈基阻燃剂", "含磷介孔杂化材料", "LD", "KDC", "PVD", "PA", "PDCP", "三聚氰胺", "二乙基次磷酸铝", "含磷介孔杂化材料"],
#         ["CN", "CB", "GR", "银粉", "镍粉", "GO", "AMGNS", "ZIF", "SiC"],
#         ["T300", "T700", "T800", "T1100", "玻璃纤维", "云母粉", "赤泥", "碳纤维"]
#     ]
# )
filler_transformer = AutoDummifier()

TRANSFORMATION_RECIPE.add(
    input_col_name = "填料种类",
    output_col_names = "Filler",
    transform = filler_transformer
)

##### "填料比例": "filler proportion"
# Parse percentage
filler_proportion_transformer = NumberExtractor(round_digits=2)

TRANSFORMATION_RECIPE.add(
    input_col_name = "填料比例",
    output_col_names = "Filler Proportion(%)",
    transform = filler_proportion_transformer
)

##### "促进剂": "accelerator"
# # One-hot encode into predefined groups
# accelerator_transformer = KeywordDummifier(
#     group_names = [
#         "accelerator_Amine-based",
#         "accelerator_Metal-salts",
#     ],
#     group_keywords = [
#         ["DMP", "二甲基苄胺", "TEA", "三乙胺", "咪唑", "UR"],
#         ["乙酸锌", "乙酰丙酮锌", "辛酸"]
#     ]
# )
accelerator_transformer = AutoDummifier()

TRANSFORMATION_RECIPE.add(
    input_col_name = "促进剂",
    output_col_names = "Accelerator",
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
    output_col_names = "Accelerator Content(%)",
    transform = accelerator_content_transformer
)

##### "温度": "temperature"
# Custom transformer
# def temperature_transformer(col: pl.Series) -> pl.Series:
#     """
#     Extract the temperature and convert to Kelvin
    
#     strange data: "室温", "常温"
#     """
#     parse_strings = col.str.extract(r'(\d+\.?\d*|温)', 1)

#     temp_expr = (
#         pl.when(parse_strings.is_null()).then(None)
#         .when(parse_strings.str.contains("温")).then(26)
#         .otherwise(parse_strings)
#         .cast(pl.Float64, strict=False)
#         .round(2)
#         + 273.15
#     ).alias("temperature(K)")
    
#     # evaluate and return expression
#     return pl.select(temp_expr).to_series()

temperature_transformer = TemperatureExtractor(
    average_mode=True,
    convert="K"
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "温度",
    output_col_names = "Temperature(K)",
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
