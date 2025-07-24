TARGETS = [
    "Fracture Toughness[MPa*m0.5]",  #Dropped
    "Flexural Strength[MPa]",
    "Flexural Modulus[MPa]",
    "Impact Strength[kJ/m2]",
    "Young Modulus[MPa]",
    "Tensile Strength[MPa]",
    "Shear Strength[MPa]", #Dropped
    "Elongation at Break[%]"
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


CONTINUOUS_RANGE = {
    'Molecular Weight[g/mol]': (50,1700),
    'Epoxy/Curing Ratio': (0.07,200),
    'Carbon Fiber[%]': (0,70),
    'Filler Proportion[%]': (0,85),
    'Temperature[K]': (273,573)
}


FINAL_TARGETS = [
    'Flexural Strength[MPa]', 
    'Flexural Modulus[MPa]',
    'Impact Strength[kJ/m2]', 
    'Young Modulus[MPa]', 
    'Tensile Strength[MPa]',
    'Elongation at Break[%]'
]


TARGETS_RANGE = {
    FINAL_TARGETS[0]: (),
    FINAL_TARGETS[1]: (),
    FINAL_TARGETS[2]: (),
    FINAL_TARGETS[3]: (),
    FINAL_TARGETS[4]: (),
    FINAL_TARGETS[5]: (0,100)
}
