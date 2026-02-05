# Raw targets map
'''
    "断裂韧性": "Fracture Toughness(MPa m0.5)", # Missing 91% of data ⛔
    "弯曲强度": "Flexural Strength(MPa)",   # Missing 51% of data 
    "弯曲模量": "Flexural Modulus(MPa)",    # Missing 74% of data ⛔
    "冲击强度": "Impact Strength(kJ/m2)",   # Missing 64% of data ⚠️
    "杨氏模量": "Young Modulus(MPa)",   # Missing 69% of data ⛔
    "拉伸强度": "Tensile Strength(MPa)",    # Missing 23% of data
    "剪切强度": "Shear Strength(MPa)", # Missing 94% of data ⛔
    "断裂伸长率": "Elongation at Break(%)"  # Missing 63% of data ⚠️
'''



# Column names
TENSILE_STRENGTH = "Tensile Strength(MPa)" #1
FLEXURAL_STRENGTH = "Flexural Strength(MPa)" #2
EPOXY = "Epoxy"
CURING = "Curing"
FILLER = "Filler"
EPOXY_EPOXY_RATIO = "Epoxy/Epoxy Ratio"
EPOXY_CURING_RATIO = "Epoxy/Curing Ratio"
FILLER_PROPORTION = "Filler Proportion(%)"
FILLER_PROPORTION_2 = "Filler Proportion 2(%)"

"Filler Proportion(%)", "Filler Proportion 2(%)", "Filler Proportion 3(%)


# Cleaned target names by completeness
TARGET_tensile_strength = "Tensile Strength(MPa)"
TARGET_flexural_strength = "Flexural Strength(MPa)"
# TARGET_elongation_at_break = "Elongation at Break(%)"
# TARGET_impact_strength = "Impact Strength(kJ/m2)"

TARGET_epoxy = "Epoxy"
TARGET_curing = "Curing"
TARGET_filler = "Filler"


TARGETS_REGRESSION = [
    TARGET_tensile_strength,
    TARGET_flexural_strength,
    # TARGET_elongation_at_break,
    # TARGET_impact_strength
]

TARGETS_CLASSIFICATION = [
    TARGET_epoxy,
    TARGET_curing,
    TARGET_filler
]
