# "calculator_id": 2
# "calculator_name": "Creatinine Clearance (Cockcroft-Gault Equation)"
CALCULATOR_2 = {
    "name": "Creatinine Clearance Calculation Using Cockcroft-Gault Equation",
    "description": "Calculate the patient's creatinine clearance (CrCl) using the Cockcroft-Gault equation, taking into account body weight adjustments based on BMI.",
    "inputs": [
        {
            "input_name": "weight_kg",
            "input_desc": "Patient's actual body weight in kg",
            "input_type": "float"
        },
        {
            "input_name": "height_m",
            "input_desc": "Patient's height in meters",
            "input_type": "float"
        },
        {
            "input_name": "gender",
            "input_desc": "Patient's gender ('male' or 'female')",
            "input_type": "string"
        },
        {
            "input_name": "height_in",
            "input_desc": "Patient's height in inches",
            "input_type": "float"
        },
        {
            "input_name": "age",
            "input_desc": "Patient's age in years",
            "input_type": "int"
        },
        {
            "input_name": "serum_creatinine_mg_dL",
            "input_desc": "Serum creatinine level in mg/dL",
            "input_type": "float"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "calculate_bmi",
            "step_description": "Calculate the patient's body mass index using their weight and height.",
            "step_inputs": [
                {
                    "input_name": "weight_kg",
                    "input_desc": "Patient's actual body weight in kg",
                    "input_type": "float",
                    "input_source": "$|inputs|.weight_kg"
                },
                {
                    "input_name": "height_m",
                    "input_desc": "Patient's height in meters",
                    "input_type": "float",
                    "input_source": "$|inputs|.height_m"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "bmi",
                    "output_desc": "Calculated BMI value",
                    "output_type": "float"
                }
            ],
            "category": "FormulaCalculation",
            "reason": "BMI calculation has a specific formula that requires patient weight and height to be computed, so we choose the FormulaCalculation category.",
            "detail": "BMI is calculated as weight divided by height squared, where weight is in kg and height is in meters.",
            "code": "def calculate_bmi(weight_kg: float, height_m: float) -> float:\n    '''\n    decs: calculate the patient's body mass index using their weight and height\n    args:\n        - weight_kg (float): patient's actual body weight in kg\n        - height_m (float): patient's height in meters\n    returns: bmi (float): calculated bmi value\n    category: FormulaCalculation\n    '''\n    bmi = weight_kg / (height_m ** 2)\n    return bmi"
        },
        {
            "step_id": "2",
            "step_name": "determine_body_weight_category",
            "step_description": "Map the BMI value to a category that dictates which body weight to use.",
            "step_inputs": [
                {
                    "input_name": "bmi",
                    "input_desc": "Calculated BMI value",
                    "input_type": "float",
                    "input_source": "$|1|.bmi"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "body_weight_category",
                    "output_desc": "Categorization of body weight: 'underweight', 'normal', 'overweight/obese'",
                    "output_type": "string"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "Body weight category determination is based on BMI value, which requires a threshold to categorize the patient's weight into different categories, so we choose the DiscreteValueMapping category.",
            "detail": "If BMI < 18.5 → 'underweight'; if 18.5 ≤ BMI ≤ 24.9 → 'normal'; if BMI > 24.9 → 'overweight/obese'.",
            "code": "def determine_body_weight_category(bmi: float) -> str:\n    '''\n    decs:map bmi value to a body weight category\n    args:\n        - bmi (float): calculated bmi value\n    returns: body_weight_category: categorization of body weight: 'underweight', 'normal', 'overweight/obese'\n    category: DiscreteValueMapping\n    '''\n    if bmi < 18.5:\n        return 'underweight'\n    elif 18.5 <= bmi <= 24.9:\n        return 'normal'\n    else:\n        return 'overweight/obese'"
        },
        {
            "step_id": "3",
            "step_name": "calculate_ibw",
            "step_description": "Calculate the patient's ideal body weight based on gender and height.",
            "step_inputs": [
                {
                    "input_name": "gender",
                    "input_desc": "Patient's gender ('male' or 'female')",
                    "input_type": "string",
                    "input_source": "$|inputs|.gender"
                },
                {
                    "input_name": "height_in",
                    "input_desc": "Patient's height in inches",
                    "input_type": "float",
                    "input_source": "$|inputs|.height_in"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "ibw_kg",
                    "output_desc": "Ideal body weight in kg",
                    "output_type": "float"
                }
            ],
            "category": "FormulaCalculation",
            "detail": "IBW for males = 50 + 2.3 × (height in inches - 60); IBW for females = 45.5 + 2.3 × (height in inches - 60).",
            "reason": "IBW calculation has a specific formula that requires patient gender and height to be computed, so we choose the FormulaCalculation category.",
            "code": "def calculate_ibw(gender: str, height_in: float) -> float:\n    '''\n    decs: Calculate the patient's ideal body weight based on gender and height\n    args:\n        - gender (str): Patient's gender ('male' or 'female')\n        - height_in (float): Patient's height in inches\n    returns: ibw_kg (float): Ideal body weight in kg\n    category: FormulaCalculation\n    '''\n    if gender == 'male':\n        ibw_kg = 50 + 2.3 * (height_in - 60)\n    elif gender == 'female':\n        ibw_kg = 45.5 + 2.3 * (height_in - 60)\n    else:\n        raise ValueError(\"Invalid gender value. Must be 'male' or 'female'.\")\n    \n    return ibw_kg"
        },
        {
            "step_id": "4",
            "step_name": "calculate_abw",
            "step_description": "Calculate the adjusted body weight based on ideal body weight and actual body weight.",
            "step_inputs": [
                {
                    "input_name": "ibw_kg",
                    "input_desc": "Ideal body weight in kg",
                    "input_type": "float",
                    "input_source": "$|3|.ibw_kg"
                },
                {
                    "input_name": "weight_kg",
                    "input_desc": "Patient's actual body weight in kg",
                    "input_type": "float",
                    "input_source": "$|inputs|.weight_kg"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "abw_kg",
                    "output_desc": "Adjusted body weight in kg",
                    "output_type": "float"
                }
            ],
            "category": "FormulaCalculation",
            "reason": "ABW calculation has a specific formula that requires patient gender and height to be computed, so we choose the FormulaCalculation category.",
            "detail": "ABW = IBW + 0.4 × (Actual weight - IBW).",
            "code": "def calculate_abw(ibw_kg: float, weight_kg: float) -> float:\n    '''\n    decs: calculate adjusted body weight based on ideal body weight and actual body weight\n    args:\n        - ibw_kg (float): ideal body weight in kg\n        - weight_kg (float): patient's actual body weight in kg\n    returns: abw_kg (float): adjusted body weight in kg\n    category: FormulaCalculation\n    '''\n    abw_kg = ibw_kg + 0.4 * (weight_kg - ibw_kg)\n    return abw_kg"
        },
        {
            "step_id": "5",
            "step_name": "select_appropriate_body_weight",
            "step_description": "Select the appropriate body weight based on the BMI category.",
            "step_inputs": [
                {
                    "input_name": "body_weight_category",
                    "input_desc": "Categorized body weight: 'underweight', 'normal', 'overweight/obese'",
                    "input_type": "string",
                    "input_source": "$|2|.body_weight_category"
                },
                {
                    "input_name": "weight_kg",
                    "input_desc": "Patient's actual body weight in kg",
                    "input_type": "float",
                    "input_source": "$|inputs|.weight_kg"
                },
                {
                    "input_name": "ibw_kg",
                    "input_desc": "Ideal body weight in kg",
                    "input_type": "float",
                    "input_source": "$|3|.ibw_kg"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "selected_weight_kg",
                    "output_desc": "Selected body weight for CrCl calculation in kg",
                    "output_type": "float"
                }
            ],
            "category": "ConditionEvaluation",
            "reason": "Body weight selection for CrCl calculation depends on BMI category, so we choose the ConditionEvaluation category.",
            "detail": "If 'underweight' → use actual weight; if 'normal' → use min(IBW, actual weight); if 'overweight/obese' → use ABW.",
            "code": "def select_appropriate_body_weight(body_weight_category: str, weight_kg: float, ibw_kg: float) -> float:\n    '''\n    decs: Select the appropriate body weight for CrCl calculation based on BMI category\n    args:\n        - body_weight_category (str): Categorized body weight: 'underweight', 'normal', 'overweight/obese'\n        - weight_kg (float): Patient's actual body weight in kg\n        - ibw_kg (float): Ideal body weight in kg\n    returns: selected_weight_kg (float): Selected body weight for CrCl calculation in kg\n    category: ConditionEvaluation\n    '''\n    if body_weight_category == 'underweight':\n        selected_weight_kg = weight_kg\n    elif body_weight_category == 'normal':\n        selected_weight_kg = min(ibw_kg, weight_kg)\n    else:  # 'overweight/obese'\n        selected_weight_kg = weight_kg\n\n    return selected_weight_kg"
        },
        {
            "step_id": "6",
            "step_name": "calculate_crcl",
            "step_description": "Compute the patient's creatinine clearance using the Cockcroft-Gault formula.",
            "step_inputs": [
                {
                    "input_name": "age",
                    "input_desc": "Patient's age in years",
                    "input_type": "int",
                    "input_source": "$|inputs|.age"
                },
                {
                    "input_name": "selected_weight_kg",
                    "input_desc": "Selected body weight for CrCl calculation in kg",
                    "input_type": "float",
                    "input_source": "$|5|.selected_weight_kg"
                },
                {
                    "input_name": "gender",
                    "input_desc": "Patient's gender ('male' or 'female')",
                    "input_type": "string",
                    "input_source": "$|inputs|.gender"
                },
                {
                    "input_name": "serum_creatinine_mg_dL",
                    "input_desc": "Serum creatinine level in mg/dL",
                    "input_type": "float",
                    "input_source": "$|inputs|.serum_creatinine_mg_dL"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "crcl_ml_min",
                    "output_desc": "Creatinine clearance in mL/min",
                    "output_type": "float"
                }
            ],
            "category": "FormulaCalculation",
            "reason": "CrCl calculation has a specific formula that requires patient age, selected body weight, gender, and serum creatinine level to be computed, so we choose the FormulaCalculation category.",
            "detail": "CrCl = ((140 - age) × selected_weight × gender_coefficient) / (72 × serum_creatinine_mg_dL), where gender_coefficient = 1 for male, 0.85 for female.",
            "code": "def calculate_crcl(age: int, selected_weight_kg: float, gender: str, serum_creatinine_mg_dL: float) -> float:\n    '''\n    decs:compute the patient's creatinine clearance using the Cockcroft-Gault formula\n    args:\n        - age (int): Patient's age in years\n        - selected_weight_kg (float): Selected body weight for CrCl calculation in kg\n        - gender (str): Patient's gender ('male' or 'female')\n        - serum_creatinine_mg_dL (float): Serum creatinine level in mg/dL\n    returns: crcl_ml_min (float): Creatinine clearance in mL/min\n    category: FormulaCalculation\n    '''\n    # determine gender coefficient\n    if gender == 'male':\n        gender_coefficient = 1.0\n    elif gender == 'female':\n        gender_coefficient = 0.85\n    else:\n        raise ValueError(\"Invalid gender value. Must be 'male' or 'female'.\")\n\n    # apply Cockcroft-Gault formula\n    crcl_ml_min = ((140 - age) * selected_weight_kg * gender_coefficient) / (72 * serum_creatinine_mg_dL)\n\n    return crcl_ml_min"
        }
    ],
    "output": {
        "output_name": "crcl_ml_min",
        "output_desc": "Creatinine clearance in mL/min",
        "output_type": "float",
        "output_source": "$|6|.crcl_ml_min"
    }
}

# "calculator_id": 5
# "calculator_name": "Mean Arterial Pressure (MAP)"
CALCULATOR_5 = {
    "name": "Mean Arterial Pressure Calculation",
    "description": "This process calculates a patient's Mean Arterial Pressure (MAP) in mm Hg using their systolic and diastolic blood pressure values recorded at the time of initial hospital admission, prior to any treatment.",
    "inputs": [
        {
            "input_name": "systolic_bp",
            "input_desc": "The patient's systolic blood pressure (SBP) at initial hospital admission, in millimeters of mercury (mm Hg).",
            "input_type": "number"
        },
        {
            "input_name": "diastolic_bp",
            "input_desc": "The patient's diastolic blood pressure (DBP) at initial hospital admission, in millimeters of mercury (mm Hg).",
            "input_type": "number"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "calculate_map",
            "step_description": "Calculate the Mean Arterial Pressure (MAP) using the standard formula based on systolic and diastolic blood pressure.",
            "step_inputs": [
                {
                    "input_name": "systolic_bp",
                    "input_desc": "The patient's systolic blood pressure (SBP) at initial hospital admission, in millimeters of mercury (mm Hg).",
                    "input_type": "number",
                    "input_source": "$|inputs|.systolic_bp"
                },
                {
                    "input_name": "diastolic_bp",
                    "input_desc": "The patient's diastolic blood pressure (DBP) at initial hospital admission, in millimeters of mercury (mm Hg).",
                    "input_type": "number",
                    "input_source": "$|inputs|.diastolic_bp"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "map_value",
                    "output_desc": "The calculated Mean Arterial Pressure (MAP), in millimeters of mercury (mm Hg).",
                    "output_type": "number"
                }
            ],
            "category": "FormulaCalculation",
            "reason": "MAP calculation has a specific formula that requires patient systolic and diastolic blood pressure to be computed, so we choose the FormulaCalculation category.",
            "detail": "Perform the calculation using the formula: MAP = (1/3) * systolic_bp + (2/3) * diastolic_bp. This is a precise numerical computation.",
            "code": "def calculate_map(systolic_bp: float, diastolic_bp: float) -> float:\n    '''\n    desc: Calculate Mean Arterial Pressure (MAP) using systolic and diastolic blood pressure\n    args:\n        - systolic_bp (float): The patient's systolic blood pressure (SBP) at initial hospital admission, in millimeters of mercury (mm Hg)\n        - diastolic_bp (float): The patient's diastolic blood pressure (DBP) at initial hospital admission, in millimeters of mercury (mm Hg)\n    returns: map_value: The calculated Mean Arterial Pressure (MAP), in millimeters of mercury (mm Hg)\n    category: FormulaCalculation\n    '''\n    import math\n    \n    map_value = (1/3) * systolic_bp + (2/3) * diastolic_bp\n    \n    return map_value"
        }
    ],
    "output": {
        "output_name": "map_value",
        "output_desc": "The calculated Mean Arterial Pressure (MAP), in millimeters of mercury (mm Hg).",
        "output_type": "number",
        "output_source": "$|1|.map_value"
    }
}

# "calculator_id": 6
# "calculator_name": "Body Mass Index (BMI)"
CALCULATOR_6 = {
    "name": "Body Mass Index Calculation",
    "description": "This process calculates a patient's Body Mass Index (BMI) using their weight and height measured upon initial hospital admission, prior to any treatment. The result is expressed in kg/m².",
    "inputs": [
        {
            "input_name": "patient_weight_kg",
            "input_desc": "The patient's body weight measured at initial hospital admission. Unit: kilograms (kg).",
            "input_type": "float"
        },
        {
            "input_name": "patient_height_m",
            "input_desc": "The patient's body height measured at initial hospital admission. Unit: meters (m).",
            "input_type": "float"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "calculate_bmi",
            "step_description": "Computes the Body Mass Index (BMI) using the formula: BMI = weight / (height * height).",
            "step_inputs": [
                {
                    "input_name": "patient_weight_kg",
                    "input_desc": "The patient's body weight. Unit: kilograms (kg).",
                    "input_type": "float",
                    "input_source": "$|inputs|.patient_weight_kg"
                },
                {
                    "input_name": "patient_height_m",
                    "input_desc": "The patient's body height. Unit: meters (m).",
                    "input_type": "float",
                    "input_source": "$|inputs|.patient_height_m"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "bmi_value",
                    "output_desc": "The calculated Body Mass Index value. Unit: kg/m².",
                    "output_type": "float"
                }
            ],
            "category": "FormulaCalculation",
            "reason": "BMI calculation has a specific formula that requires patient weight and height to be computed, so we choose the FormulaCalculation category.",
            "detail": "The Body Mass Index (BMI) is calculated by dividing the patient's weight in kilograms by the square of their height in meters: bmi_value = patient_weight_kg / (patient_height_m * patient_height_m).",
            "code": "def calculate_bmi(patient_weight_kg: float, patient_height_m: float) -> float:\n    '''\n    desc: Computes the Body Mass Index (BMI) using the formula: BMI = weight / (height * height).\n    args:\n        - patient_weight_kg (float): The patient's body weight. Unit: kilograms (kg).\n        - patient_height_m (float): The patient's body height. Unit: meters (m).\n    returns: bmi_value: The calculated Body Mass Index value. Unit: kg/m².\n    category: anthropometric_calculation\n    '''\n    \n    bmi_value = patient_weight_kg / (patient_height_m * patient_height_m)\n    \n    return bmi_value"
        }
    ],
    "output": {
        "output_name": "bmi_value",
        "output_desc": "The patient's calculated Body Mass Index (BMI). Unit: kg/m².",
        "output_type": "float",
        "output_source": "$|1|.bmi_value"
    }
}

# "calculator_id": 68
# "calculator_name": "Estimated of Conception"
CALCULATOR_68 = {
    "name": "Estimated Date of Conception Calculation",
    "description": "This calculation process estimates a patient's date of conception based on their Last Menstrual Period (LMP) date. The standard medical formula adds 14 days (2 weeks) to the LMP date to account for the typical time from the start of the menstrual cycle to ovulation and fertilization.",
    "inputs": [
        {
            "input_name": "last_menstrual_period_date",
            "input_desc": "The first day of the patient's last menstrual period. Format: MM/DD/YYYY (U.S. date format).",
            "input_type": "str"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "Parse LMP Date",
            "step_description": "Convert the input LMP date string into a structured date object for calculation.",
            "step_inputs": [
                {
                    "input_name": "last_menstrual_period_date",
                    "input_desc": "The first day of the patient's last menstrual period. Format: MM/DD/YYYY (U.S. date format).",
                    "input_type": "str",
                    "input_source": "$|inputs|.last_menstrual_period_date"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "lmp_date_obj",
                    "output_desc": "The LMP date represented as a structured date object.",
                    "output_type": "datetime.date"
                }
            ],
            "category": "TimeSeriesProcessing",
            "reason": "This step parses a date string (MM/DD/YYYY) into a structured date object, which involves time data parsing and conversion operations. According to the category definition, TimeSeriesProcessing handles operations on time data including format conversion, making it the most appropriate choice.",
            "detail": "Parse the input string 'last_menstrual_period_date' (e.g., '08/15/2023') using a date parsing function that expects the MM/DD/YYYY format. This creates a date object containing year, month, and day components.",
            "code": "def parse_lmp_date(last_menstrual_period_date: str) -> datetime.date:\n    '''\n    desc: Parse LMP date string into a structured date object\n    args:\n        - last_menstrual_period_date (str): The first day of the patient's last menstrual period. Format: MM/DD/YYYY (U.S. date format).\n    returns: lmp_date_obj: The LMP date represented as a structured date object\n    category: Data Preparation\n    '''\n    import datetime\n    \n    lmp_date_obj = datetime.datetime.strptime(last_menstrual_period_date, '%m/%d/%Y').date()\n    return lmp_date_obj"
        },
        {
            "step_id": "2",
            "step_name": "Add Gestational Offset",
            "step_description": "Add the standard gestational offset of 14 days (2 weeks) to the LMP date to estimate the date of conception.",
            "step_inputs": [
                {
                    "input_name": "lmp_date_obj",
                    "input_desc": "The LMP date represented as a structured date object.",
                    "input_type": "datetime.date",
                    "input_source": "$|1|.lmp_date_obj"
                },
                {
                    "input_name": "gestational_offset_days",
                    "input_desc": "The number of days to add to the LMP date. Default value is 14, representing 2 weeks.",
                    "input_type": "int",
                    "input_source": None
                }
            ],
            "step_outputs": [
                {
                    "output_name": "conception_date_obj",
                    "output_desc": "The estimated date of conception represented as a structured date object.",
                    "output_type": "datetime.date"
                }
            ],
            "category": "TimeSeriesProcessing",
            "reason": "This step performs a date arithmetic operation by adding a timedelta (14 days) to a date object. This is a time series operation that manipulates date data, which aligns with the TimeSeriesProcessing category definition for performing operations on time data such as date difference calculations.",
            "detail": "Add the timedelta of 'gestational_offset_days' (default 14) to the 'lmp_date_obj' to calculate the 'conception_date_obj'. This operation estimates the date of conception by adding 2 weeks (14 days) to the LMP date.",
            "code": "def add_gestational_offset(lmp_date_obj: datetime.date, gestational_offset_days: int = 14) -> datetime.date:\n    '''\n    desc: Add gestational offset days to LMP date to estimate conception date\n    args:\n        - lmp_date_obj (datetime.date): The LMP date represented as a structured date object\n        - gestational_offset_days (int): The number of days to add to the LMP date. Default value is 14, representing 2 weeks\n    returns: conception_date_obj: The estimated date of conception represented as a structured date object\n    category: Core Calculation\n    '''\n    \n    offset = datetime.timedelta(days=gestational_offset_days)\n    conception_date_obj = lmp_date_obj + offset\n    \n    return conception_date_obj"
        },
        {
            "step_id": "3",
            "step_name": "Format Output Date",
            "step_description": "Convert the calculated conception date object back into the required string format (MM/DD/YYYY).",
            "step_inputs": [
                {
                    "input_name": "conception_date_obj",
                    "input_desc": "The estimated date of conception represented as a structured date object.",
                    "input_type": "datetime.date",
                    "input_source": "$|2|.conception_date_obj"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "estimated_conception_date",
                    "output_desc": "The final estimated date of conception in MM/DD/YYYY string format.",
                    "output_type": "str"
                }
            ],
            "category": "TimeSeriesProcessing",
            "reason": "This step converts a date object back to a formatted string (MM/DD/YYYY), which is a time data format conversion operation. The TimeSeriesProcessing category explicitly covers format conversion of time data, making it the correct classification for this step.",
            "detail": "Format the 'conception_date_obj' into a string using the format specifier '%m/%d/%Y' to produce the final output in the MM/DD/YYYY format (e.g., '08/29/2023').",
            "code": "def format_output_date(conception_date_obj: datetime.date) -> str:\n    '''\n    desc: Convert the conception date object to MM/DD/YYYY string format\n    args:\n        - conception_date_obj (datetime.date): The estimated date of conception represented as a structured date object\n    returns: estimated_conception_date: The final estimated date of conception in MM/DD/YYYY string format\n    category: Result Formatting\n    '''\n    \n    estimated_conception_date = conception_date_obj.strftime('%m/%d/%Y')\n    \n    return estimated_conception_date"
        }
    ],
    "output": {
        "output_name": "estimated_conception_date",
        "output_desc": "The patient's estimated date of conception based on their last menstrual period, formatted as MM/DD/YYYY.",
        "output_type": "str",
        "output_source": "$|3|.estimated_conception_date"
    }
}

# "calculator_id": 48
# "calculator_name": "PERC Rule for Pulmonary Embolism"
CALCULATOR_48 = {
    "name": "PERC Rule for Pulmonary Embolism Calculation",
    "description": "Calculates the number of criteria met according to the PERC (Pulmonary Embolism Rule-out Criteria) Rule for Pulmonary Embolism. The calculation uses the patient's medical values and health status at the time of initial hospital admission, prior to any treatment.",
    "inputs": [
        {
            "input_name": "age",
            "input_desc": "Patient's age in years",
            "input_type": "number"
        },
        {
            "input_name": "heart_rate",
            "input_desc": "Patient's heart rate in beats per minute (bpm)",
            "input_type": "number"
        },
        {
            "input_name": "o2_saturation",
            "input_desc": "Patient's oxygen saturation on room air, measured as a percentage (%)",
            "input_type": "number"
        },
        {
            "input_name": "unilateral_leg_swelling",
            "input_desc": "Presence of unilateral leg swelling. Enum values: 'yes', 'no'",
            "input_type": "string"
        },
        {
            "input_name": "hemoptysis",
            "input_desc": "Presence of hemoptysis (coughing up blood). Enum values: 'yes', 'no'",
            "input_type": "string"
        },
        {
            "input_name": "recent_surgery_trauma",
            "input_desc": "History of recent surgery or trauma within the past 4 weeks, requiring general anesthesia. Enum values: 'yes', 'no'",
            "input_type": "string"
        },
        {
            "input_name": "prior_pe_dvt",
            "input_desc": "History of prior pulmonary embolism (PE) or deep vein thrombosis (DVT). Enum values: 'yes', 'no'",
            "input_type": "string"
        },
        {
            "input_name": "hormone_use",
            "input_desc": "Current hormone use (e.g., oral contraceptives, hormone replacement therapy, or estrogenic hormones). Enum values: 'yes', 'no'",
            "input_type": "string"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "Evaluate PERC Criteria",
            "step_description": "Evaluates each of the 8 PERC Rule criteria based on patient inputs and assigns a score of 0 or 1 for each criterion.",
            "step_inputs": [
                {
                    "input_name": "age",
                    "input_desc": "Patient's age in years",
                    "input_type": "number",
                    "input_source": "$|inputs|.age"
                },
                {
                    "input_name": "heart_rate",
                    "input_desc": "Patient's heart rate in beats per minute (bpm)",
                    "input_type": "number",
                    "input_source": "$|inputs|.heart_rate"
                },
                {
                    "input_name": "o2_saturation",
                    "input_desc": "Patient's oxygen saturation on room air (%)",
                    "input_type": "number",
                    "input_source": "$|inputs|.o2_saturation"
                },
                {
                    "input_name": "unilateral_leg_swelling",
                    "input_desc": "Presence of unilateral leg swelling. Enum values: 'yes', 'no'",
                    "input_type": "string",
                    "input_source": "$|inputs|.unilateral_leg_swelling"
                },
                {
                    "input_name": "hemoptysis",
                    "input_desc": "Presence of hemoptysis. Enum values: 'yes', 'no'",
                    "input_type": "string",
                    "input_source": "$|inputs|.hemoptysis"
                },
                {
                    "input_name": "recent_surgery_trauma",
                    "input_desc": "Recent surgery/trauma (within 4 weeks). Enum values: 'yes', 'no'",
                    "input_type": "string",
                    "input_source": "$|inputs|.recent_surgery_trauma"
                },
                {
                    "input_name": "prior_pe_dvt",
                    "input_desc": "History of prior PE or DVT. Enum values: 'yes', 'no'",
                    "input_type": "string",
                    "input_source": "$|inputs|.prior_pe_dvt"
                },
                {
                    "input_name": "hormone_use",
                    "input_desc": "Current hormone use. Enum values: 'yes', 'no'",
                    "input_type": "string",
                    "input_source": "$|inputs|.hormone_use"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "criteria_scores",
                    "output_desc": "List of scores (0 or 1) for the 8 PERC criteria",
                    "output_type": "list[number]"
                }
            ],
            "category": "ConditionEvaluation",
            "reason": "This step evaluates the 8 PERC Rule criteria based on patient inputs and assigns a score of 0 or 1 for each criterion. The ConditionEvaluation category is appropriate as it deals with evaluating conditions or criteria.",
            "detail": "For each PERC criterion, perform a conditional check: 1) If age >= 50, assign 1, else 0. 2) If heart_rate >= 100, assign 1, else 0. 3) If o2_saturation < 95, assign 1, else 0. 4) If unilateral_leg_swelling == 'yes', assign 1, else 0. 5) If hemoptysis == 'yes', assign 1, else 0. 6) If recent_surgery_trauma == 'yes', assign 1, else 0. 7) If prior_pe_dvt == 'yes', assign 1, else 0. 8) If hormone_use == 'yes', assign 1, else 0. Return a list containing these 8 scores in the order of the criteria.",
            "code": "def evaluate_perc_criteria(age: int, heart_rate: int, o2_saturation: float, unilateral_leg_swelling: str, hemoptysis: str, recent_surgery_trauma: str, prior_pe_dvt: str, hormone_use: str) -> list[int]:\n    '''\n    desc: Evaluates each of the 8 PERC Rule criteria based on patient inputs and assigns a score of 0 or 1 for each criterion.\n    args:\n        - age (int): Patient's age in years\n        - heart_rate (int): Patient's heart rate in beats per minute (bpm)\n        - o2_saturation (float): Patient's oxygen saturation on room air (%)\n        - unilateral_leg_swelling (str): Presence of unilateral leg swelling. Enum values: 'yes', 'no'\n        - hemoptysis (str): Presence of hemoptysis. Enum values: 'yes', 'no'\n        - recent_surgery_trauma (str): Recent surgery/trauma (within 4 weeks). Enum values: 'yes', 'no'\n        - prior_pe_dvt (str): History of prior PE or DVT. Enum values: 'yes', 'no'\n        - hormone_use (str): Current hormone use. Enum values: 'yes', 'no'\n    returns: criteria_scores: List of scores (0 or 1) for the 8 PERC criteria\n    category: ConditionEvaluation\n    '''\n\n    criteria_scores = []\n    \n    # Criterion 1: Age\n    if age >= 50:\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 2: Heart rate\n    if heart_rate >= 100:\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 3: Oxygen saturation\n    if o2_saturation < 95:\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 4: Unilateral leg swelling\n    if unilateral_leg_swelling == 'yes':\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 5: Hemoptysis\n    if hemoptysis == 'yes':\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 6: Recent surgery/trauma\n    if recent_surgery_trauma == 'yes':\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 7: Prior PE or DVT\n    if prior_pe_dvt == 'yes':\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    # Criterion 8: Hormone use\n    if hormone_use == 'yes':\n        criteria_scores.append(1)\n    else:\n        criteria_scores.append(0)\n    \n    return criteria_scores"
        },
        {
            "step_id": "2",
            "step_name": "Calculate Total Score",
            "step_description": "Sums the individual criterion scores to obtain the total number of PERC criteria met.",
            "step_inputs": [
                {
                    "input_name": "criteria_scores",
                    "input_desc": "List of scores (0 or 1) for the 8 PERC criteria",
                    "input_type": "list[number]",
                    "input_source": "$|1|.criteria_scores"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "total_criteria_met",
                    "output_desc": "Total number of PERC criteria met",
                    "output_type": "number"
                }
            ],
            "category": "StatisticalAggregation",
            "reason": "This step sums the individual criterion scores to obtain the total number of PERC criteria met. The StatisticalAggregation category is appropriate as it deals with aggregating or summarizing numerical data.",
            "detail": "Calculate the sum of all elements in the input list 'criteria_scores': total_criteria_met = sum(criteria_scores).",
            "code": "def calculate_total_score(criteria_scores: list[int]) -> int:\n    '''\n    desc: Calculate the sum of all elements in the input list to obtain the total number of PERC criteria met\n    args:\n        - criteria_scores (list[int]): List of scores (0 or 1) for the 8 PERC criteria\n    returns: total_criteria_met: Total number of PERC criteria met\n    category: StatisticalAggregation\n    '''\n    \n    total_criteria_met = sum(criteria_scores)\n    \n    return total_criteria_met"
        }
    ],
    "output": {
        "output_name": "total_criteria_met",
        "output_desc": "Total number of PERC criteria met",
        "output_type": "number",
        "output_source": "$|2|.total_criteria_met"
    }
}

# "calculator_id": 8
# "calculator_name": "Wells' Criteria for Pulmonary Embolism"
CALCULATOR_8 = {
    "name": "Wells' Criteria for Pulmonary Embolism Calculation",
    "description": "This process calculates the Wells' Criteria score for Pulmonary Embolism (PE) risk assessment based on patient clinical data at initial hospital admission prior to any treatment. The score is the sum of points assigned to seven clinical criteria.",
    "inputs": [
        {
            "input_name": "clinical_signs_of_dvt",
            "input_desc": "Presence of clinical signs and symptoms of Deep Vein Thrombosis (DVT). Enum values: 'yes', 'no'.",
            "input_type": "string"
        },
        {
            "input_name": "pe_is_primary_diagnosis",
            "input_desc": "Whether Pulmonary Embolism (PE) is the number one diagnosis or equally likely. Enum values: 'yes', 'no'.",
            "input_type": "string"
        },
        {
            "input_name": "heart_rate",
            "input_desc": "Patient's heart rate, in beats per minute (bpm).",
            "input_type": "float"
        },
        {
            "input_name": "immobilization_or_surgery",
            "input_desc": "Immobilization for at least 3 days OR surgery within the previous 4 weeks. Enum values: 'yes', 'no'.",
            "input_type": "string"
        },
        {
            "input_name": "previous_pe_or_dvt",
            "input_desc": "History of previous, objectively diagnosed PE or DVT. Enum values: 'yes', 'no'.",
            "input_type": "string"
        },
        {
            "input_name": "hemoptysis",
            "input_desc": "Presence of hemoptysis (coughing up blood). Enum values: 'yes', 'no'.",
            "input_type": "string"
        },
        {
            "input_name": "malignancy",
            "input_desc": "Malignancy with treatment within the past 6 months or palliative status. Enum values: 'yes', 'no'.",
            "input_type": "string"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "score_clinical_signs_of_dvt",
            "step_description": "Assign points based on the presence of clinical signs and symptoms of DVT.",
            "step_inputs": [
                {
                    "input_name": "clinical_signs_of_dvt",
                    "input_desc": "Presence of clinical signs and symptoms of Deep Vein Thrombosis (DVT). Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.clinical_signs_of_dvt"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "dvt_score",
                    "output_desc": "Assigned points for DVT criterion.",
                    "output_type": "float"
                }
            ],
            "category": "criterion_scoring",
            "reason": "This step assigns points based on the presence of clinical signs and symptoms of DVT. The criterion_scoring category is appropriate as it deals with assigning points or scores to individual criteria.",
            "detail": "If clinical_signs_of_dvt is 'yes', assign 3.0 points. If 'no', assign 0.0 points.",
            "code": "def score_clinical_signs_of_dvt(clinical_signs_of_dvt: str) -> float:\n    '''\n    desc: Assign points based on the presence of clinical signs and symptoms of DVT.\n    args:\n        - clinical_signs_of_dvt (str): Presence of clinical signs and symptoms of Deep Vein Thrombosis (DVT). Enum values: 'yes', 'no'.\n    returns: dvt_score: Assigned points for DVT criterion.\n    category: criterion_scoring\n    '''\n    \n    if clinical_signs_of_dvt == 'yes':\n        dvt_score = 3.0\n    elif clinical_signs_of_dvt == 'no':\n        dvt_score = 0.0\n    else:\n        # Handle unexpected input by returning 0.0\n        dvt_score = 0.0\n    \n    return dvt_score"
        },
        {
            "step_id": "2",
            "step_name": "score_pe_as_primary_diagnosis",
            "step_description": "Assign points based on whether PE is the primary or equally likely diagnosis.",
            "step_inputs": [
                {
                    "input_name": "pe_is_primary_diagnosis",
                    "input_desc": "Whether Pulmonary Embolism (PE) is the number one diagnosis or equally likely. Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.pe_is_primary_diagnosis"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "primary_diagnosis_score",
                    "output_desc": "Assigned points for primary diagnosis criterion.",
                    "output_type": "float"
                }
            ],
            "category": "",
            "reason": "This step assigns points based on whether PE is the primary or equally likely diagnosis. The criterion_scoring category is appropriate as it deals with assigning points or scores to individual criteria.",
            "detail": "If pe_is_primary_diagnosis is 'yes', assign 3.0 points. If 'no', assign 0.0 points.",
            "code": "def score_pe_as_primary_diagnosis(pe_is_primary_diagnosis: str) -> float:\n    '''\n    desc: Assign points based on whether PE is the primary or equally likely diagnosis.\n    args:\n        - pe_is_primary_diagnosis (str): Whether Pulmonary Embolism (PE) is the number one diagnosis or equally likely. Enum values: 'yes', 'no'.\n    returns: primary_diagnosis_score: Assigned points for primary diagnosis criterion.\n    category: criterion_scoring\n    '''\n    \n    if pe_is_primary_diagnosis == 'yes':\n        return 3.0\n    else:\n        return 0.0"
        },
        {
            "step_id": "3",
            "step_name": "score_heart_rate",
            "step_description": "Assign points based on whether the patient's heart rate is greater than 100 bpm.",
            "step_inputs": [
                {
                    "input_name": "heart_rate",
                    "input_desc": "Patient's heart rate, in beats per minute (bpm).",
                    "input_type": "float",
                    "input_source": "$|inputs|.heart_rate"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "heart_rate_score",
                    "output_desc": "Assigned points for heart rate criterion.",
                    "output_type": "float"
                }
            ],
            "category": "ThresholdMapping",
            "reason": "This step assigns points based on whether the patient's heart rate is greater than 100 bpm. The ThresholdMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined thresholds.",
            "detail": "If heart_rate > 100, assign 1.5 points. Otherwise, assign 0.0 points.",
            "code": "def score_heart_rate(heart_rate: float) -> float:\n    '''\n    desc: Assign points based on whether the patient's heart rate is greater than 100 bpm.\n    args:\n        - heart_rate (float): Patient's heart rate, in beats per minute (bpm).\n    returns: heart_rate_score (float): Assigned points for heart rate criterion.\n    category: criterion_scoring\n    '''\n    \n    if heart_rate > 100:\n        heart_rate_score = 1.5\n    else:\n        heart_rate_score = 0.0\n    \n    return heart_rate_score"
        },
        {
            "step_id": "4",
            "step_name": "score_immobilization_or_surgery",
            "step_description": "Assign points based on recent immobilization or surgery.",
            "step_inputs": [
                {
                    "input_name": "immobilization_or_surgery",
                    "input_desc": "Immobilization for at least 3 days OR surgery within the previous 4 weeks. Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.immobilization_or_surgery"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "immobilization_score",
                    "output_desc": "Assigned points for immobilization/surgery criterion.",
                    "output_type": "float"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on recent immobilization or surgery. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If immobilization_or_surgery is 'yes', assign 1.5 points. If 'no', assign 0.0 points.",
            "code": "def score_immobilization_or_surgery(immobilization_or_surgery: str) -> float:\n    '''\n    desc: Assign points based on recent immobilization or surgery.\n    args:\n        - immobilization_or_surgery (str): Immobilization for at least 3 days OR surgery within the previous 4 weeks. Enum values: 'yes', 'no'.\n    returns: immobilization_score: Assigned points for immobilization/surgery criterion.\n    category: criterion_scoring\n    '''\n    \n    if immobilization_or_surgery == 'yes':\n        return 1.5\n    elif immobilization_or_surgery == 'no':\n        return 0.0\n    else:\n        # Handle unexpected input values\n        raise ValueError(f\"Invalid value for immobilization_or_surgery: {immobilization_or_surgery}. Expected 'yes' or 'no'.\")"
        },
        {
            "step_id": "5",
            "step_name": "score_previous_pe_or_dvt",
            "step_description": "Assign points based on history of previous PE or DVT.",
            "step_inputs": [
                {
                    "input_name": "previous_pe_or_dvt",
                    "input_desc": "History of previous, objectively diagnosed PE or DVT. Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.previous_pe_or_dvt"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "history_score",
                    "output_desc": "Assigned points for history criterion.",
                    "output_type": "float"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on history of previous PE or DVT. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If previous_pe_or_dvt is 'yes', assign 1.5 points. If 'no', assign 0.0 points.",
            "code": "def score_previous_pe_or_dvt(previous_pe_or_dvt: str) -> float:\n    '''\n    desc: Assign points based on history of previous PE or DVT.\n    args:\n        - previous_pe_or_dvt (str): History of previous, objectively diagnosed PE or DVT. Enum values: 'yes', 'no'.\n    returns: history_score: Assigned points for history criterion.\n    category: criterion_scoring\n    '''\n    \n    if previous_pe_or_dvt == 'yes':\n        history_score = 1.5\n    elif previous_pe_or_dvt == 'no':\n        history_score = 0.0\n    else:\n        # 如果输入不是预期的值，可以返回0.0或抛出异常\n        # 根据业务逻辑，这里返回0.0\n        history_score = 0.0\n    \n    return history_score"
        },
        {
            "step_id": "6",
            "step_name": "score_hemoptysis",
            "step_description": "Assign points based on the presence of hemoptysis.",
            "step_inputs": [
                {
                    "input_name": "hemoptysis",
                    "input_desc": "Presence of hemoptysis (coughing up blood). Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.hemoptysis"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "hemoptysis_score",
                    "output_desc": "Assigned points for hemoptysis criterion.",
                    "output_type": "float"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on the presence of hemoptysis. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If hemoptysis is 'yes', assign 1.0 points. If 'no', assign 0.0 points.",
            "code": "def score_hemoptysis(hemoptysis: str) -> float:\n    '''\n    desc: Assign points based on the presence of hemoptysis.\n    args:\n        - hemoptysis (str): Presence of hemoptysis (coughing up blood). Enum values: 'yes', 'no'.\n    returns: hemoptysis_score: Assigned points for hemoptysis criterion.\n    category: criterion_scoring\n    '''\n    \n    if hemoptysis == 'yes':\n        hemoptysis_score = 1.0\n    elif hemoptysis == 'no':\n        hemoptysis_score = 0.0\n    else:\n        # Handle unexpected input by returning 0.0\n        hemoptysis_score = 0.0\n    \n    return hemoptysis_score"
        },
        {
            "step_id": "7",
            "step_name": "score_malignancy",
            "step_description": "Assign points based on recent or palliative malignancy.",
            "step_inputs": [
                {
                    "input_name": "malignancy",
                    "input_desc": "Malignancy with treatment within the past 6 months or palliative status. Enum values: 'yes', 'no'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.malignancy"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "malignancy_score",
                    "output_desc": "Assigned points for malignancy criterion.",
                    "output_type": "float"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on recent or palliative malignancy. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If malignancy is 'yes', assign 1.0 points. If 'no', assign 0.0 points.",
            "code": "def score_malignancy(malignancy: str) -> float:\n    '''\n    desc: Assign points based on recent or palliative malignancy.\n    args:\n        - malignancy (str): Malignancy with treatment within the past 6 months or palliative status. Enum values: 'yes', 'no'.\n    returns: malignancy_score: Assigned points for malignancy criterion.\n    category: criterion_scoring\n    '''\n    \n    if malignancy == 'yes':\n        malignancy_score = 1.0\n    elif malignancy == 'no':\n        malignancy_score = 0.0\n    else:\n        # Handle unexpected input by returning 0.0\n        malignancy_score = 0.0\n    \n    return malignancy_score"
        },
        {
            "step_id": "8",
            "step_name": "calculate_total_wells_score",
            "step_description": "Sum all individual criterion scores to obtain the total Wells' Criteria score.",
            "step_inputs": [
                {
                    "input_name": "dvt_score",
                    "input_desc": "Assigned points for DVT criterion.",
                    "input_type": "float",
                    "input_source": "$|1|.dvt_score"
                },
                {
                    "input_name": "primary_diagnosis_score",
                    "input_desc": "Assigned points for primary diagnosis criterion.",
                    "input_type": "float",
                    "input_source": "$|2|.primary_diagnosis_score"
                },
                {
                    "input_name": "heart_rate_score",
                    "input_desc": "Assigned points for heart rate criterion.",
                    "input_type": "float",
                    "input_source": "$|3|.heart_rate_score"
                },
                {
                    "input_name": "immobilization_score",
                    "input_desc": "Assigned points for immobilization/surgery criterion.",
                    "input_type": "float",
                    "input_source": "$|4|.immobilization_score"
                },
                {
                    "input_name": "history_score",
                    "input_desc": "Assigned points for history criterion.",
                    "input_type": "float",
                    "input_source": "$|5|.history_score"
                },
                {
                    "input_name": "hemoptysis_score",
                    "input_desc": "Assigned points for hemoptysis criterion.",
                    "input_type": "float",
                    "input_source": "$|6|.hemoptysis_score"
                },
                {
                    "input_name": "malignancy_score",
                    "input_desc": "Assigned points for malignancy criterion.",
                    "input_type": "float",
                    "input_source": "$|7|.malignancy_score"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "total_wells_score",
                    "output_desc": "Total Wells' Criteria score for Pulmonary Embolism risk.",
                    "output_type": "float"
                }
            ],
            "category": "StatisticalAggregation",
            "reason": "This step sums all individual criterion scores to obtain the total Wells' Criteria score. The StatisticalAggregation category is appropriate as it deals with aggregating multiple input values to produce a single output value.",
            "detail": "total_wells_score = dvt_score + primary_diagnosis_score + heart_rate_score + immobilization_score + history_score + hemoptysis_score + malignancy_score",
            "code": "def calculate_total_wells_score(dvt_score: float, primary_diagnosis_score: float, heart_rate_score: float, immobilization_score: float, history_score: float, hemoptysis_score: float, malignancy_score: float) -> float:\n    '''\n    desc: Calculate total Wells' Criteria score by summing all individual criterion scores.\n    args:\n        - dvt_score (float): Assigned points for DVT criterion.\n        - primary_diagnosis_score (float): Assigned points for primary diagnosis criterion.\n        - heart_rate_score (float): Assigned points for heart rate criterion.\n        - immobilization_score (float): Assigned points for immobilization/surgery criterion.\n        - history_score (float): Assigned points for history criterion.\n        - hemoptysis_score (float): Assigned points for hemoptysis criterion.\n        - malignancy_score (float): Assigned points for malignancy criterion.\n    returns: total_wells_score (float): Total Wells' Criteria score for Pulmonary Embolism risk.\n    category: aggregation\n    '''\n    \n    total_wells_score = dvt_score + primary_diagnosis_score + heart_rate_score + immobilization_score + history_score + hemoptysis_score + malignancy_score\n    \n    return total_wells_score"
        }
    ],
    "output": {
        "output_name": "total_wells_score",
        "output_desc": "Total Wells' Criteria score for Pulmonary Embolism risk.",
        "output_type": "float",
        "output_source": "$|8|.total_wells_score"
    }
}

# "calculator_id": 15,
# "calculator_name": "Child-Pugh Score for Cirrhosis Mortality",
CALCULATOR_15 = {
    "name": "Child-Pugh Score for Cirrhosis Mortality Calculation",
    "description": "This process calculates the Child-Pugh Score for a patient with cirrhosis based on five clinical criteria: total bilirubin, serum albumin, INR, ascites, and hepatic encephalopathy. The score is the sum of points assigned to each criterion and is used to assess the severity of liver disease and mortality risk.",
    "inputs": [
        {
            "input_name": "total_bilirubin",
            "input_desc": "Patient's total bilirubin level. Unit: mg/dL. Acceptable values: numeric.",
            "input_type": "float"
        },
        {
            "input_name": "albumin",
            "input_desc": "Patient's serum albumin level. Unit: g/dL. Acceptable values: numeric.",
            "input_type": "float"
        },
        {
            "input_name": "inr",
            "input_desc": "Patient's International Normalized Ratio (INR). Acceptable values: numeric.",
            "input_type": "float"
        },
        {
            "input_name": "ascites",
            "input_desc": "Presence and severity of ascites. Acceptable values: 'absent', 'slight', 'moderate'.",
            "input_type": "string"
        },
        {
            "input_name": "encephalopathy",
            "input_desc": "Grade of hepatic encephalopathy. Acceptable values: 'none', 'grade_1_2', 'grade_3_4'.",
            "input_type": "string"
        }
    ],
    "steps": [
        {
            "step_id": "1",
            "step_name": "score_bilirubin",
            "step_description": "Assigns points based on the patient's total bilirubin level.",
            "step_inputs": [
                {
                    "input_name": "total_bilirubin",
                    "input_desc": "Patient's total bilirubin level. Unit: mg/dL.",
                    "input_type": "float",
                    "input_source": "$|inputs|.total_bilirubin"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "bilirubin_score",
                    "output_desc": "Points assigned for the bilirubin criterion (1, 2, or 3).",
                    "output_type": "int"
                }
            ],
            "category": "ThresholdMapping",
            "reason": "This step assigns points based on the patient's total bilirubin level. The ThresholdMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined thresholds.",
            "detail": "If total_bilirubin < 2, assign 1 point. If 2 <= total_bilirubin <= 3, assign 2 points. If total_bilirubin > 3, assign 3 points.",
            "code": "def score_bilirubin(total_bilirubin: float) -> int:\n    '''\n    desc: Assigns points based on the patient's total bilirubin level.\n    args:\n        - total_bilirubin (float): Patient's total bilirubin level. Unit: mg/dL.\n    returns: bilirubin_score (int): Points assigned for the bilirubin criterion (1, 2, or 3).\n    category: scoring\n    '''\n    \n    if total_bilirubin < 2:\n        bilirubin_score = 1\n    elif total_bilirubin <= 3:\n        bilirubin_score = 2\n    else:\n        bilirubin_score = 3\n    \n    return bilirubin_score"
        },
        {
            "step_id": "2",
            "step_name": "score_albumin",
            "step_description": "Assigns points based on the patient's serum albumin level.",
            "step_inputs": [
                {
                    "input_name": "albumin",
                    "input_desc": "Patient's serum albumin level. Unit: g/dL.",
                    "input_type": "float",
                    "input_source": "$|inputs|.albumin"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "albumin_score",
                    "output_desc": "Points assigned for the albumin criterion (1, 2, or 3).",
                    "output_type": "int"
                }
            ],
            "category": "ThresholdMapping",
            "reason": "This step assigns points based on the patient's serum albumin level. The ThresholdMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined thresholds.",
            "detail": "If albumin > 3.5, assign 1 point. If 2.8 <= albumin <= 3.5, assign 2 points. If albumin < 2.8, assign 3 points.",
            "code": "def score_albumin(albumin: float) -> int:\n    '''\n    desc: Assigns points based on the patient's serum albumin level.\n    args:\n        - albumin (float): Patient's serum albumin level. Unit: g/dL.\n    returns: albumin_score (int): Points assigned for the albumin criterion (1, 2, or 3).\n    category: scoring\n    '''\n    \n    if albumin > 3.5:\n        albumin_score = 1\n    elif albumin >= 2.8 and albumin <= 3.5:\n        albumin_score = 2\n    else:\n        albumin_score = 3\n    \n    return albumin_score"
        },
        {
            "step_id": "3",
            "step_name": "score_inr",
            "step_description": "Assigns points based on the patient's INR value.",
            "step_inputs": [
                {
                    "input_name": "inr",
                    "input_desc": "Patient's International Normalized Ratio (INR).",
                    "input_type": "float",
                    "input_source": "$|inputs|.inr"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "inr_score",
                    "output_desc": "Points assigned for the INR criterion (1, 2, or 3).",
                    "output_type": "int"
                }
            ],
            "category": "ThresholdMapping",
            "reason": "This step assigns points based on the patient's INR value. The ThresholdMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined thresholds.",
            "detail": "If inr < 1.7, assign 1 point. If 1.7 <= inr <= 2.3, assign 2 points. If inr > 2.3, assign 3 points.",
            "code": "def score_inr(inr: float) -> int:\n    '''\n    desc: Assigns points based on the patient's INR value.\n    args:\n        - inr (float): Patient's International Normalized Ratio (INR).\n    returns: inr_score: Points assigned for the INR criterion (1, 2, or 3).\n    category: scoring\n    '''\n    \n    if inr < 1.7:\n        inr_score = 1\n    elif 1.7 <= inr <= 2.3:\n        inr_score = 2\n    else:  # inr > 2.3\n        inr_score = 3\n    \n    return inr_score"
        },
        {
            "step_id": "4",
            "step_name": "score_ascites",
            "step_description": "Assigns points based on the presence and severity of ascites.",
            "step_inputs": [
                {
                    "input_name": "ascites",
                    "input_desc": "Presence and severity of ascites. Values: 'absent', 'slight', 'moderate'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.ascites"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "ascites_score",
                    "output_desc": "Points assigned for the ascites criterion (1, 2, or 3).",
                    "output_type": "int"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on the presence and severity of ascites. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If ascites is 'absent', assign 1 point. If ascites is 'slight', assign 2 points. If ascites is 'moderate', assign 3 points.",
            "code": "def score_ascites(ascites: str) -> int:\n    '''\n    desc: Assigns points based on the presence and severity of ascites.\n    args:\n        - ascites (str): Presence and severity of ascites. Values: 'absent', 'slight', 'moderate'.\n    returns: ascites_score: Points assigned for the ascites criterion (1, 2, or 3).\n    category: scoring\n    '''\n    \n    if ascites == 'absent':\n        return 1\n    elif ascites == 'slight':\n        return 2\n    elif ascites == 'moderate':\n        return 3\n    else:\n        # Handle unexpected input by returning a default value or raising an error\n        # Based on the specification, we'll return 0 for unexpected values\n        return 0"
        },
        {
            "step_id": "5",
            "step_name": "score_encephalopathy",
            "step_description": "Assigns points based on the grade of hepatic encephalopathy.",
            "step_inputs": [
                {
                    "input_name": "encephalopathy",
                    "input_desc": "Grade of hepatic encephalopathy. Values: 'none', 'grade_1_2', 'grade_3_4'.",
                    "input_type": "string",
                    "input_source": "$|inputs|.encephalopathy"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "encephalopathy_score",
                    "output_desc": "Points assigned for the encephalopathy criterion (1, 2, or 3).",
                    "output_type": "int"
                }
            ],
            "category": "DiscreteValueMapping",
            "reason": "This step assigns points based on the grade of hepatic encephalopathy. The DiscreteValueMapping category is appropriate as it deals with mapping input values to corresponding output values based on predefined discrete categories.",
            "detail": "If encephalopathy is 'none', assign 1 point. If encephalopathy is 'grade_1_2', assign 2 points. If encephalopathy is 'grade_3_4', assign 3 points.",
            "code": "def score_encephalopathy(encephalopathy: str) -> int:\n    '''\n    desc: Assigns points based on the grade of hepatic encephalopathy.\n    args:\n        - encephalopathy (str): Grade of hepatic encephalopathy. Values: 'none', 'grade_1_2', 'grade_3_4'.\n    returns: encephalopathy_score: Points assigned for the encephalopathy criterion (1, 2, or 3).\n    category: scoring\n    '''\n    if encephalopathy == 'none':\n        encephalopathy_score = 1\n    elif encephalopathy == 'grade_1_2':\n        encephalopathy_score = 2\n    elif encephalopathy == 'grade_3_4':\n        encephalopathy_score = 3\n    else:\n        raise ValueError(f\"Invalid encephalopathy grade: {encephalopathy}. Must be 'none', 'grade_1_2', or 'grade_3_4'.\")\n    \n    return encephalopathy_score"
        },
        {
            "step_id": "6",
            "step_name": "sum_scores",
            "step_description": "Calculates the total Child-Pugh Score by summing the points from all five criteria.",
            "step_inputs": [
                {
                    "input_name": "bilirubin_score",
                    "input_desc": "Points from the bilirubin criterion.",
                    "input_type": "int",
                    "input_source": "$|1|.bilirubin_score"
                },
                {
                    "input_name": "albumin_score",
                    "input_desc": "Points from the albumin criterion.",
                    "input_type": "int",
                    "input_source": "$|2|.albumin_score"
                },
                {
                    "input_name": "inr_score",
                    "input_desc": "Points from the INR criterion.",
                    "input_type": "int",
                    "input_source": "$|3|.inr_score"
                },
                {
                    "input_name": "ascites_score",
                    "input_desc": "Points from the ascites criterion.",
                    "input_type": "int",
                    "input_source": "$|4|.ascites_score"
                },
                {
                    "input_name": "encephalopathy_score",
                    "input_desc": "Points from the encephalopathy criterion.",
                    "input_type": "int",
                    "input_source": "$|5|.encephalopathy_score"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "child_pugh_score",
                    "output_desc": "The total Child-Pugh Score (sum of points from all criteria).",
                    "output_type": "int"
                }
            ],
            "category": "StatisticalAggregation",
            "reason": "This step calculates the total Child-Pugh Score by summing the points from all five criteria. The StatisticalAggregation category is appropriate as it deals with aggregating multiple input values to produce a single output value.",
            "detail": "child_pugh_score = bilirubin_score + albumin_score + inr_score + ascites_score + encephalopathy_score",
            "code": "def sum_scores(bilirubin_score: int, albumin_score: int, inr_score: int, ascites_score: int, encephalopathy_score: int) -> int:\n    '''\n    desc: Calculates the total Child-Pugh Score by summing the points from all five criteria.\n    args:\n        - bilirubin_score (int): Points from the bilirubin criterion.\n        - albumin_score (int): Points from the albumin criterion.\n        - inr_score (int): Points from the INR criterion.\n        - ascites_score (int): Points from the ascites criterion.\n        - encephalopathy_score (int): Points from the encephalopathy criterion.\n    returns: child_pugh_score (int): The total Child-Pugh Score (sum of points from all criteria).\n    category: aggregation\n    '''\n    child_pugh_score = bilirubin_score + albumin_score + inr_score + ascites_score + encephalopathy_score\n    return child_pugh_score"
        }
    ],
    "output": {
        "output_name": "child_pugh_score",
        "output_desc": "The calculated total Child-Pugh Score.",
        "output_type": "int",
        "output_source": "$|6|.child_pugh_score"
    }
}