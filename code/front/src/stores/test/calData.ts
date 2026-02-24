const CAL_O2 = {
    "calculator_id": 2,
    "calculator_name": "Creatinine Clearance (Cockcroft-Gault Equation)",
    "category": "lab",
    "output_type": "decimal",
    "question": "What is the patient's Creatinine Clearance using the Cockroft-Gault Equation in terms of mL/min",
    // "question": "What is the patient's Creatinine Clearance using the Cockroft-Gault Equation in terms of mL/min? You should use the patient's adjusted body weight in kg instead of the patient's actual body weight if the patient is overweight or obese based on their BMI. If the patient's BMI's normal, set their adjusted body weight to the minimum of the ideal body and actual weight. If the patient is underweight, please set their adjusted body weight to their actual body weight.",
    "formula": "The formula for computing Creatinine Clearance (CrCl) using the Cockcroft-Gault Equation is:\nCrCl (mL/min) = ((140 - age) x weight x gender_coefficient) / (72 x serum creatinine in mg/dL),\nwhere gender_coefficient = 1 if male, 0.85 if female, and the weight used depends on BMI as follows: if BMI < 18.5 (underweight), use actual body weight; if BMI is between 18.5 and 24.9 (normal weight), use ideal body weight (IBW); if BMI ≥ 25 (overweight/obese), use adjusted body weight (ABW).\nThe formula for computing the patient's body mass index (BMI) is (weight)/(height * height), where weight is the patient's weight in kg and height is the patient's height in m.\nIdeal body weight is calculated using the Devine formula:\nIBW (kg) = 50 + 2.3 x (height in inches - 60) for males,\nIBW (kg) = 45.5 + 2.3 x (height in inches - 60) for females.\nAdjusted body weight is calculated as: ABW (kg) = IBW + 0.4 x (actual body weight - IBW)."
}


const CAL_O5 = {
    "calculator_id": 5,
    "calculator_name": "Mean Arterial Pressure (MAP)",
    "category": "physical",
    "output_type": "decimal",
    "question": "What is patient's mean arterial pressure in mm Hg?",
    "formula": "The mean arterial pressure is computed by the formula 1/3 * (systolic blood pressure) + 2/3 * (diastolic blood pressure)"
}


const CAL_O6 = {
    "calculator_id": 6,
    "calculator_name": "Body Mass Index (BMI)",
    "category": "physical",
    "output_type": "decimal",
    "question": "What is the patient's body mass mass index (BMI)? Your answer should be in terms of kg/m².",
    "formula": "The formula for computing the patient's body mass index (BMI) is (weight)/(height * height), where weight is the patient's weight in kg and height is the patient's height in m."
}

const CAL_68 = {
    "calculator_id": 68,
    "calculator_name": "Estimated of Conception",
    "category": "date",
    "output_type": "date",
    "question": "Based on the patient's last menstrual period and cycle length, what is the the patient's estimated date of conception?",
    "formula": "The patient's estimated date of conception based on their last period is computed by adding to 2 weeks to the patient's last menstrual period date. All dates are expressed in U.S. format (MM/DD/YYYY)."
}

const CAL_48 = {
    "calculator_id": 48,
    "calculator_name": "PERC Rule for Pulmonary Embolism",
    "category": "diagnosis",
    "output_type": "integer",
    "question": "What are the number of criteria met for the PERC Rule for Pulmonary Embolism (PE)?",
    "formula": "The PERC Rule critiera are listed below:\n\n1. Age ≥50: No = 0 points, Yes = +1 point\n2. Heart Rate (HR) ≥100: No = 0 points, Yes = +1 point\n3. O₂ saturation on room air <95%: No = 0 points, Yes = +1 point\n4. Unilateral leg swelling: No = 0 points, Yes = +1 point\n5. Hemoptysis: No = 0 points, Yes = +1 point\n6. Recent surgery or trauma (within 4 weeks, requiring treatment with general anesthesia): No = 0 points, Yes = +1 point\n7. Prior pulmonary embolism (PE) or deep vein thrombosis (DVT): No = 0 points, Yes = +1 point\n8. Hormone use (oral contraceptives, hormone replacement, or estrogenic hormone use in males or females): No = 0 points, Yes = +1 point\n\nThe total number of criteria met is taken by summing the points for each criterion."
}

const CAL_8 = {
    "calculator_id": 8,
    "calculator_name": "Wells' Criteria for Pulmonary Embolism",
    "category": "risk",
    "output_type": "decimal",
    "question": "What is the patient’s score of Wells' criteria for Pulmonary Embolism?",
    "formula": "The criteria for the Wells' Criteria for Pulmonary Embolism score are listed below:\n\n1. Clinical signs and symptoms of DVT: No = 0 points, Yes = +3 points\n2. PE is #1 diagnosis OR equally likely: No = 0 points, Yes = +3 points\n3. Heart rate > 100: No = 0 points, Yes = +1.5 points\n4. Immobilization at least 3 days OR surgery in the previous 4 weeks: No = 0 points, Yes = +1.5 points\n5. Previous, objectively diagnosed PE or DVT: No = 0 points, Yes = +1.5 points\n6. Hemoptysis: No = 0 points, Yes = +1 point\n7. Malignancy with treatment within 6 months or palliative: No = 0 points, Yes = +1 point\n\nThe total score is calculated by summing the points for each criterion."
}

const CAL_15 = {
    "calculator_id": 15,
    "calculator_name": "Child-Pugh Score for Cirrhosis Mortality",
    "category": "severity",
    "output_type": "integer",
    "question": "What is the patient's Child-Pugh Score?",
    "formula": "The criteria for the Child-Pugh Score are listed below:\n\n1. Bilirubin (Total): <2 mg/dL (<34.2 μmol/L) = +1 point, 2-3 mg/dL (34.2-51.3 μmol/L) = +2 points, >3 mg/dL (>51.3 μmol/L) = +3 points\n2. Albumin: >3.5 g/dL (>35 g/L) = +1 point, 2.8-3.5 g/dL (28-35 g/L) = +2 points, <2.8 g/dL (<28 g/L) = +3 points\n3. INR: <1.7 = +1 point, 1.7-2.3 = +2 points, >2.3 = +3 points\n4. Ascites: Absent = +1 point, Slight = +2 points, Moderate = +3 points\n5. Encephalopathy: No Encephalopathy = +1 point, Grade 1-2 = +2 points, Grade 3-4 = +3 points \n(Grade 0: normal consciousness, personality, neurological examination, electroencephalogram\nGrade 1: restless, sleep disturbed, irritable/agitated, tremor, impaired handwriting, 5 cps waves\nGrade 2: lethargic, time-disoriented, inappropriate, asterixis, ataxia, slow triphasic waves\nGrade 3: somnolent, stuporous, place-disoriented, hyperactive reflexes, rigidity, slower waves\nGrade 4: unrousable coma, no personality/behavior, decerebrate, slow 2-3 cps delta activity)\n\nThe Child-Pugh Score is calculated by summing the points for each criterion."
}

export const QuestionLibrary = {
    "CAL_2": CAL_O2,
    "CAL_5": CAL_O5,
    "CAL_6": CAL_O6,
    "CAL_68": CAL_68,
    "CAL_48": CAL_48,
    "CAL_8": CAL_8,
    "CAL_15": CAL_15,
}