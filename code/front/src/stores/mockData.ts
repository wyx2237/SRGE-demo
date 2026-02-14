// src/stores/mockData.ts

export const mockRule = {
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
      "reason": "Requires mapping a continuous numerical value (BMI) into discrete categorical labels (underweight, normal, etc.).",
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
      "reason": "Requires mapping a continuous numerical value (BMI) into discrete categorical labels (underweight, normal, etc.).",
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
      "reason": "Requires mapping a continuous numerical value (height) into a discrete categorical label (gender) to calculate the ideal body weight.",
      "detail": "IBW for males = 50 + 2.3 × (height in inches - 60); IBW for females = 45.5 + 2.3 × (height in inches - 60).",
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
      "reason": "Requires mapping a continuous numerical value (actual weight) into a discrete categorical label (body weight category) to calculate the adjusted body weight.",
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
      "reason": "Requires mapping a continuous numerical value (age, weight, creatinine) into a discrete categorical label (gender) to calculate the creatinine clearance.",
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
      "reason": "Requires mapping a continuous numerical value (age, weight, creatinine) into a discrete categorical label (gender) to calculate the creatinine clearance.",
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
};


export const mockClinicalText = `Patient is a 58-year-old male admitted for routine checkup. 
His height is 178 cm (approx 70 inches) and his actual body weight is 95 kg. 
Recent laboratory results indicate a Serum Creatinine level of 1.2 mg/dL. 
No history of liver disease.`;



// src/stores/mockData.ts

// ... (之前的 mockCockcroftGaultRule 和 mockClinicalText 保持不变)

// 新增：8个原子工具的定义
export const atomicTools = [
  {
    id: "tool_001",
    general_info: {
      Name: "FormulaCalculation",
      Description: "Formula calculation category, primarily performing calculations for specific mathematical formulas, involving precise and complex numerical computations."
    },
    flow_info: {
      Input: "Input should include all variables required to calculate the formula; in most cases, each input parameter is a single element.",
      Output: "The output parameter should be a clear single variable, typically of a general type (number/string/boolean)."
    },
    code_info: {
      Language: "python",
      Library: "math",
      Logic: "1. Import necessary calculation libraries, such as math.\n2. Convert formula strings into Python-executable expressions."
    }
  },
  {
    id: "tool_002",
    general_info: {
      Name: "ConditionEvaluation",
      Description: "Condition evaluation category, primarily performing condition expressions evaluation, outputting predefined condition result values."
    },
    flow_info: {
      Input: "Input should be the variables required to evaluate the condition expression; each input parameter is a single element.",
      Output: "The output parameter should be a clear single variable, typically of a general type."
    },
    code_info: {
      Language: "python",
      Logic: "1. Use if-else statements to implement condition branches.\n2. Each condition branch should return the corresponding result value."
    },
  },
  {
    id: "tool_003",
    general_info: {
      Name: "DiscreteValueMapping",
      Description: "Discrete value mapping category, primarily mapping finite input values to predefined output values (e.g., status code conversion)."
    },
    flow_info: {
      Input: "Input should be a discrete value (e.g., number, string, or enum value).",
      Output: "The output should be the mapped value from the mapping table."
    },
    code_info: {
      Language: "python",
      Logic: "1. Check the input value against the keys in the mapping table dictionary.\n2. Return corresponding value or default."
    },
  },
  {
    id: "tool_004",
    general_info: {
      Name: "UnitConversion",
      Description: "Unit conversion category, primarily converting numerical values from one unit to another (e.g., m → inches)."
    },
    flow_info: {
      Input: "Input should be the numerical value in the original unit.",
      Output: "The output should be the numerical value converted to the target unit."
    },
    code_info: {
      Language: "python",
      Logic: "1. Check the input value against conversion coefficients.\n2. Perform conversion calculation."
    },
  },
  {
    id: "tool_005",
    general_info: {
      Name: "StatisticalAggregation",
      Description: "Statistical aggregation category, primarily performing statistical calculations on a set of data (e.g., sum, average, max)."
    },
    flow_info: {
      Input: "Input should be a set of numerical data (usually a list of numbers).",
      Output: "The output should be the aggregated statistical result."
    },
    code_info: {
      Language: "python",
      Logic: "1. Validate input data.\n2. Perform aggregation calculation (sum, avg, etc.)."
    },
  },
  {
    id: "tool_006",
    general_info: {
      Name: "LogicalCombination",
      Description: "Logical combination category, primarily performing logical operations on a set of boolean values (AND, OR, NOT)."
    },
    flow_info: {
      Input: "Input should be a set of boolean values.",
      Output: "The output should be the result of the logical expression (boolean)."
    },
    code_info: {
      Language: "python",
      Logic: "1. Validate boolean inputs.\n2. Perform logical calculation."
    },
  },
  {
    id: "tool_007",
    general_info: {
      Name: "TimeSeriesProcessing",
      Description: "Time series processing category, performing operations on time data (e.g., date difference, format conversion)."
    },
    flow_info: {
      Input: "Input should be a set of time series data (usually strings).",
      Output: "The output should be the processed time series data."
    },
    code_info: {
      Language: "python",
      Logic: "1. Parse input time strings.\n2. Perform time series operation."
    },
  },
  {
    id: "tool_008",
    general_info: {
      Name: "ThresholdMapping",
      Description: "Threshold mapping category, mapping continuous numerical values to discrete values based on thresholds."
    },
    flow_info: {
      Input: "Input should be a set of numerical data.",
      Output: "The output should be the mapped value (e.g., category label)."
    },
    code_info: {
      Language: "python",
      Logic: "1. Compare input against threshold ranges.\n2. Return corresponding mapped value."
    },
  }
];