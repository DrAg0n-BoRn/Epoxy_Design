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

# Cleaned target names by completeness
TARGET_tensile_strength = "Tensile Strength(MPa)"
TARGET_flexural_strength = "Flexural Strength(MPa)"
TARGET_elongation_at_break = "Elongation at Break(%)"
TARGET_impact_strength = "Impact Strength(kJ/m2)"

