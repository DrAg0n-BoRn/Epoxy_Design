### Raw data
RAW_TARGETS = [
    "断裂韧性",
    "弯曲强度",
    "弯曲模量",
    "冲击强度",
    "杨氏模量",
    "拉伸强度",
    "剪切强度",
    "断裂伸长率"
]

TARGETS = [
    "Fracture Toughness(MPa m0.5)",  #Dropped
    "Flexural Strength(MPa)",
    "Flexural Modulus(MPa)",
    "Impact Strength(kJ/m2)",
    "Young Modulus(MPa)",
    "Tensile Strength(MPa)",
    "Shear Strength(MPa)", #Dropped
    "Elongation at Break(%)"
]

OPTIMIZATION_TARGETS = [
    "Flexural Strength(MPa)",
    "Flexural Modulus(MPa)",
    "Impact Strength(kJ/m2)",
    "Young Modulus(MPa)",
    "Tensile Strength(MPa)",
    "Elongation at Break(%)"
]

### Value ranges
TARGETS_RANGE = {
    "Flexural Strength(MPa)": (0,7400),
    "Flexural Modulus(MPa)": (0,200000),
    "Impact Strength(kJ/m2)": (0,400),
    "Young Modulus(MPa)": (0,300000),
    "Tensile Strength(MPa)": (0,6000),
    "Elongation at Break(%)": (0,400)
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

### Machine Learning
MODEL_HIDDEN_LAYERS = [550,450,350,250,150,50]

MODEL_INITIAL_LEARNING_RATE = 0.001

MODEL_DROP_OUT_RATE = 0.2

MODEL_TEST_SIZE = 0.2

### Optimization
OPTIMIZATION_HIDDEN_LAYERS = [120, 90, 60, 30]

OPTIMIZATION_INITIAL_LEARNING_RATE = 0.001

OPTIMIZATION_DROP_OUT_RATE = 0.2

OPTIMIZATION_TEST_SIZE = 0.2
