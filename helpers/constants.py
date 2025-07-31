### Raw data
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


### Preprocess data
FINAL_TARGETS = [
    'Flexural Strength(MPa)', 
    'Flexural Modulus(MPa)',
    'Impact Strength(kJ/m2)', 
    'Young Modulus(MPa)', 
    'Tensile Strength(MPa)',
    'Elongation at Break(%)'
]

NUMBER_FEATURES = 20

NUMBER_BINARY_FEATURES = 15


### Allowed Value ranges
CONTINUOUS_RANGE = {
    'Molecular Weight(g/mol)': (50,1700),
    'Epoxy/Curing Ratio': (1,200),
    'Carbon Fiber(%)': (0,70),
    'Filler Proportion(%)': (0,85),
    'Temperature(K)': (273,573)
}

TARGETS_RANGE = {
    FINAL_TARGETS[0]: (0,7400),
    FINAL_TARGETS[1]: (0,200000),
    FINAL_TARGETS[2]: (0,400),
    FINAL_TARGETS[3]: (0,300000),
    FINAL_TARGETS[4]: (0,6000),
    FINAL_TARGETS[5]: (0,400)
}


### OPTIMAL value ranges
CONTINUOUS_RANGE_OPTIMAL = {
    'Molecular Weight(g/mol)': (50,1700),
    'Epoxy/Curing Ratio': (0.07,200),
    'Carbon Fiber(%)': (0,70),
    'Filler Proportion(%)': (0,85),
    'Temperature(K)': (273,573)
}

TARGETS_RANGE_OPTIMAL = {
    FINAL_TARGETS[0]: (),
    FINAL_TARGETS[1]: (),
    FINAL_TARGETS[2]: (),
    FINAL_TARGETS[3]: (),
    FINAL_TARGETS[4]: (),
    FINAL_TARGETS[5]: (0,100)
}


### Machine Learning
MODEL_HIDDEN_LAYERS = [200,150,100,50,20]

INITIAL_LEARNING_RATE = 0.001

DROP_OUT_RATE = 0.2
