# Raw targets map
'''
    "断裂韧性": "Fracture Toughness(MPa m0.5)", # Missing 91% of data ⛔
    "弯曲强度": "Flexural Strength(MPa)",   # Missing 51% of data ⚠️
    "弯曲模量": "Flexural Modulus(MPa)",    # Missing 74% of data ⛔
    "冲击强度": "Impact Strength(kJ/m2)",   # Missing 64% of data ⚠️
    "杨氏模量": "Young Modulus(MPa)",   # Missing 69% of data ⛔
    "拉伸强度": "Tensile Strength(MPa)",    # Missing 23% of data ✅
    "剪切强度": "Shear Strength(MPa)", # Missing 94% of data ⛔
    "断裂伸长率": "Elongation at Break(%)"  # Missing 63% of data ⚠️
'''


# Column names
TENSILE_STRENGTH = "Tensile Strength(MPa)" #1
FLEXURAL_STRENGTH = "Flexural Strength(MPa)" #2
ELONGATION_AT_BREAK = "Elongation at Break(%)" #3 ⚠️
IMPACT_STRENGTH = "Impact Strength(kJ/m2)" #4 ⚠️
EPOXY = "Epoxy"
CURING = "Curing"
FILLER = "Filler"
EPOXY_EPOXY_RATIO = "Epoxy/Epoxy Ratio"
EPOXY_CURING_RATIO = "Epoxy/Curing Ratio"
FILLER_PROPORTION = "Filler Proportion(%)"
FILLER_PROPORTION_2 = "Filler Proportion 2(%)"
FILLER_PROPORTION_3 = "Filler Proportion 3(%)"
TEMPERATURE = "Temperature(K)"


# Targets
TARGETS_REGRESSION = [
    TENSILE_STRENGTH,
    FLEXURAL_STRENGTH,
]

TARGETS_CLASSIFICATION = [
    EPOXY,
    CURING,
    FILLER
]
