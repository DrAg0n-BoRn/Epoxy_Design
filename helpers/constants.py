# Raw targets map
RAW_TARGETS = {
    "断裂韧性": "Fracture Toughness(MPa m0.5)", # Missing 91% of data (REMOVED)
    "弯曲强度": "Flexural Strength(MPa)",   # Missing 51% of data
    "弯曲模量": "Flexural Modulus(MPa)",    # Missing 74% of data (REMOVED)
    "冲击强度": "Impact Strength(kJ/m2)",   # Missing 64% of data
    "杨氏模量": "Young Modulus(MPa)",   # Missing 69% of data (REMOVED)
    "拉伸强度": "Tensile Strength(MPa)",    # Missing 23% of data
    "剪切强度": "Shear Strength(MPa)", # Missing 94% of data (REMOVED)
    "断裂伸长率": "Elongation at Break(%)"  # Missing 63% of data
}

# Cleaned target names
TARGET_flexural_strength = "Flexural Strength(MPa)"
TARGET_impact_strength = "Impact Strength(kJ/m2)"
TARGET_tensile_strength = "Tensile Strength(MPa)"
TARGET_elongation_at_break = "Elongation at Break(%)"

TARGETS = [
    TARGET_flexural_strength,
    TARGET_impact_strength,
    TARGET_tensile_strength,
    TARGET_elongation_at_break
]

### Value ranges
TARGETS_RANGE = {
    TARGET_flexural_strength: (0,7400),
    # TARGET_flexural_modulus: (0,200000),
    TARGET_impact_strength: (0,400),
    # TARGET_young_modulus: (0,300000),
    TARGET_tensile_strength: (0,6000),
    TARGET_elongation_at_break: (0,400)
}

CONTINUOUS_RANGE = {
    'Epoxy/Curing Ratio': (1,200),
    'Carbon Fiber(%)': (0,70),
    'Filler Proportion(%)': (0,85),
    'Temperature(K)': (273,573)
}

OPTIMIZATION_CONTINUOUS_RANGE = {
    'Epoxy/Curing Ratio': (1,200),
    'Carbon Fiber(%)': (0,70),
    'Filler Proportion(%)': (0,85),
    'Temperature(K)': (273,573)
}
