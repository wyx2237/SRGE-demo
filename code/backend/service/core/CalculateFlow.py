## 计算流程执行器
"""
完整计算流程格式示例：

{
    "name": "Sequential Organ Failure Assessment (SOFA) Score",
    "description": "计算患者的序贯器官衰竭评估（SOFA）评分，该评分用于评估重症监护病房（ICU）患者的器官功能障碍程度，通过六个器官系统的得分求和得出总分，范围0-24分，分数越高表示器官衰竭越严重。",
    "inputs": [
        {
            "input_name": "pao2_fio2_ratio",
            "input_desc": "PaO₂/FiO₂比值（mm Hg），反映呼吸功能",
            "input_type": "number"
        },
        {
            "input_name": "respiratory_support",
            "input_desc": "是否接受呼吸支持（布尔值，对于PaO₂/FiO₂比值<200的情况必需）",
            "input_type": "boolean"
        },
        {
            "input_name": "platelets",
            "input_desc": "血小板计数（x10³/µL），反映血液系统功能",
            "input_type": "number"
        },
        {
            "input_name": "gcs",
            "input_desc": "格拉斯哥昏迷评分（GCS，3-15分），反映神经系统功能",
            "input_type": "number"
        },
        {
            "input_name": "bilirubin",
            "input_desc": "胆红素水平（mg/dL），反映肝脏功能",
            "input_type": "number"
        },
        {
            "input_name": "map",
            "input_desc": "平均动脉压（mmHg），反映心血管功能",
            "input_type": "number"
        },
        {
            "input_name": "dopamine_dose",
            "input_desc": "多巴胺剂量（mcg/kg/min），用于心血管评分",
            "input_type": "number"
        },
        {
            "input_name": "dobutamine_dose",
            "input_desc": "多巴酚丁胺剂量（mcg/kg/min），用于心血管评分",
            "input_type": "number"
        },
        {
            "input_name": "epinephrine_dose",
            "input_desc": "肾上腺素剂量（mcg/kg/min），用于心血管评分",
            "input_type": "number"
        },
        {
            "input_name": "norepinephrine_dose",
            "input_desc": "去甲肾上腺素剂量（mcg/kg/min），用于心血管评分",
            "input_type": "number"
        },
        {
            "input_name": "creatinine",
            "input_desc": "肌酐水平（mg/dL），反映肾脏功能",
            "input_type": "number"
        },
        {
            "input_name": "urine_output",
            "input_desc": "尿量（mL/day），用于肾脏评分（可选，但肌酐在临界范围时可能影响评分）",
            "input_type": "number"
        }
    ],
    "steps": [
        {
            "step_id": 1,
            "step_name": "PaO2_FiO2_ratio_score",
            "step_description": "根据PaO₂/FiO₂比值（mm Hg）计算呼吸系统得分",
            "step_inputs": [
                {
                    "input_name": "pao2_fio2_ratio",
                    "input_desc": "PaO₂/FiO₂比值（mm Hg）",
                    "input_type": "number",
                    "input_source": "$|inputs|.pao2_fio2_ratio"
                },
                {
                    "input_name": "respiratory_support",
                    "input_desc": "是否接受呼吸支持（对于比值<200的情况需要此参数）",
                    "input_type": "boolean",
                    "input_source": "$|inputs|.respiratory_support"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "respiratory_score",
                    "output_desc": "呼吸系统得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ThresholdMapping",
            "detail": "根据PaO₂/FiO₂比值和呼吸支持状态进行阈值映射：≥400=0分，300-399=1分，200-299=2分，100-199且接受呼吸支持=3分，<100且接受呼吸支持=4分。如果比值<200但没有呼吸支持，则无法计算完整SOFA评分。",
            "code": "def calculate_respiratory_score(pao2_fio2_ratio: float, respiratory_support: bool) -> int:\n    '''\n    desc: 根据PaO₂/FiO₂比值和呼吸支持状态计算呼吸系统得分\n    args:\n        - pao2_fio2_ratio (float): PaO₂/FiO₂比值（mm Hg）\n        - respiratory_support (bool): 是否接受呼吸支持（对于比值<200的情况需要此参数）\n    returns: respiratory_score: 呼吸系统得分（0-4分）\n    category: ThresholdMapping\n    '''\n\n    # 从最高阈值开始判断\n    if pao2_fio2_ratio >= 400:\n        # 比值≥400，得0分\n        respiratory_score = 0\n    elif pao2_fio2_ratio >= 300:\n        # 比值300-399，得1分\n        respiratory_score = 1\n    elif pao2_fio2_ratio >= 200:\n        # 比值200-299，得2分\n        respiratory_score = 2\n    elif pao2_fio2_ratio >= 100 and respiratory_support:\n        # 比值100-199且接受呼吸支持，得3分\n        respiratory_score = 3\n    elif pao2_fio2_ratio < 100 and respiratory_support:\n        # 比值<100且接受呼吸支持，得4分\n        respiratory_score = 4\n    else:\n        # 比值<200但没有呼吸支持，无法计算完整SOFA评分\n        # 根据规范，这种情况下应该返回一个特殊值或抛出异常\n        # 这里返回-1表示无法计算\n        respiratory_score = -1\n\n    return respiratory_score"
        },
        {
            "step_id": 2,
            "step_name": "Platelets_score",
            "step_description": "根据血小板计数（x10³/µL）计算血液系统得分",
            "step_inputs": [
                {
                    "input_name": "platelets",
                    "input_desc": "血小板计数（x10³/µL）",
                    "input_type": "number",
                    "input_source": "$|inputs|.platelets"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "platelets_score",
                    "output_desc": "血小板得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ThresholdMapping",
            "detail": "根据血小板计数进行阈值映射：≥150=0分，100-149=1分，50-99=2分，20-49=3分，<20=4分。",
            "code": "def platelets_score(platelets: float) -> int:\n    '''\n    desc: 根据血小板计数（x10³/µL）计算血液系统得分\n    args:\n        - platelets (float): 血小板计数（x10³/µL）\n    returns: platelets_score: 血小板得分（0-4分）\n    category: ThresholdMapping\n    '''\n\n    # 从最高阈值开始判断：≥150=0分\n    if platelets >= 150:\n        platelets_score = 0\n    # 100-149=1分\n    elif platelets >= 100:\n        platelets_score = 1\n    # 50-99=2分\n    elif platelets >= 50:\n        platelets_score = 2\n    # 20-49=3分\n    elif platelets >= 20:\n        platelets_score = 3\n    # <20=4分\n    else:\n        platelets_score = 4\n\n    return platelets_score"
        },
        {
            "step_id": 3,
            "step_name": "GCS_score",
            "step_description": "根据格拉斯哥昏迷评分（GCS）计算神经系统得分",
            "step_inputs": [
                {
                    "input_name": "gcs",
                    "input_desc": "格拉斯哥昏迷评分（3-15分）",
                    "input_type": "number",
                    "input_source": "$|inputs|.gcs"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "gcs_score",
                    "output_desc": "神经系统得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ThresholdMapping",
            "detail": "根据GCS评分进行阈值映射：15=0分，13-14=1分，10-12=2分，6-9=3分，<6=4分。",
            "code": "def gcs_score(gcs: int) -> int:\n    '''\n    desc: 根据格拉斯哥昏迷评分（GCS）计算神经系统得分\n    args:\n        - gcs (int): 格拉斯哥昏迷评分（3-15分）\n    returns: gcs_score: 神经系统得分（0-4分）\n    category: ThresholdMapping\n    '''\n\n    # 从最高阈值开始判断\n    if gcs == 15:\n        # GCS为15分时，神经系统得分为0\n        gcs_score = 0\n    elif 13 <= gcs <= 14:\n        # GCS在13-14分之间时，神经系统得分为1\n        gcs_score = 1\n    elif 10 <= gcs <= 12:\n        # GCS在10-12分之间时，神经系统得分为2\n        gcs_score = 2\n    elif 6 <= gcs <= 9:\n        # GCS在6-9分之间时，神经系统得分为3\n        gcs_score = 3\n    else:\n        # GCS小于6分时，神经系统得分为4\n        gcs_score = 4\n\n    return gcs_score"
        },
        {
            "step_id": 4,
            "step_name": "Bilirubin_score",
            "step_description": "根据胆红素水平（mg/dL）计算肝脏系统得分",
            "step_inputs": [
                {
                    "input_name": "bilirubin",
                    "input_desc": "胆红素水平（mg/dL）",
                    "input_type": "number",
                    "input_source": "$|inputs|.bilirubin"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "bilirubin_score",
                    "output_desc": "肝脏系统得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ThresholdMapping",
            "detail": "根据胆红素水平进行阈值映射：<1.2=0分，1.2-1.9=1分，2.0-5.9=2分，6.0-11.9=3分，≥12.0=4分。",
            "code": "def bilirubin_score(bilirubin: float) -> int:\n    '''\n    desc: 根据胆红素水平（mg/dL）计算肝脏系统得分\n    args:\n        - bilirubin (float): 胆红素水平（mg/dL）\n    returns: bilirubin_score: 肝脏系统得分（0-4分）\n    category: ThresholdMapping\n    '''\n\n    # 从最高阈值开始判断\n    if bilirubin >= 12.0:\n        # 胆红素≥12.0 mg/dL，得4分\n        bilirubin_score = 4\n    elif bilirubin >= 6.0:\n        # 胆红素6.0-11.9 mg/dL，得3分\n        bilirubin_score = 3\n    elif bilirubin >= 2.0:\n        # 胆红素2.0-5.9 mg/dL，得2分\n        bilirubin_score = 2\n    elif bilirubin >= 1.2:\n        # 胆红素1.2-1.9 mg/dL，得1分\n        bilirubin_score = 1\n    else:\n        # 胆红素<1.2 mg/dL，得0分\n        bilirubin_score = 0\n\n    return bilirubin_score"
        },
        {
            "step_id": 5,
            "step_name": "Cardiovascular_score",
            "step_description": "根据平均动脉压（MAP）和血管活性药物使用情况计算心血管系统得分",
            "step_inputs": [
                {
                    "input_name": "map",
                    "input_desc": "平均动脉压（mmHg）",
                    "input_type": "number",
                    "input_source": "$|inputs|.map"
                },
                {
                    "input_name": "dopamine_dose",
                    "input_desc": "多巴胺剂量（mcg/kg/min）",
                    "input_type": "number",
                    "input_source": "$|inputs|.dopamine_dose"
                },
                {
                    "input_name": "dobutamine_dose",
                    "input_desc": "多巴酚丁胺剂量（mcg/kg/min）",
                    "input_type": "number",
                    "input_source": "$|inputs|.dobutamine_dose"
                },
                {
                    "input_name": "epinephrine_dose",
                    "input_desc": "肾上腺素剂量（mcg/kg/min）",
                    "input_type": "number",
                    "input_source": "$|inputs|.epinephrine_dose"
                },
                {
                    "input_name": "norepinephrine_dose",
                    "input_desc": "去甲肾上腺素剂量（mcg/kg/min）",
                    "input_type": "number",
                    "input_source": "$|inputs|.norepinephrine_dose"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "cardiovascular_score",
                    "output_desc": "心血管系统得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ConditionEvaluation",
            "detail": "根据复杂的条件逻辑进行评估：1. 无低血压（MAP≥70且无血管活性药物）=0分；2. MAP<70 mmHg=1分；3. 多巴胺≤5或任何剂量的多巴酚丁胺=2分；4. 多巴胺>5或肾上腺素≤0.1或去甲肾上腺素≤0.1=3分；5. 多巴胺>15或肾上腺素>0.1或去甲肾上腺素>0.1=4分。需要按优先级顺序评估这些条件。",
            "code": "def calculate_cardiovascular_score(map: float, dopamine_dose: float, dobutamine_dose: float, epinephrine_dose: float, norepinephrine_dose: float) -> int:\n    '''\n    desc: 根据平均动脉压（MAP）和血管活性药物使用情况计算心血管系统得分（0-4分）\n    args:\n        - map (float): 平均动脉压（mmHg）\n        - dopamine_dose (float): 多巴胺剂量（mcg/kg/min）\n        - dobutamine_dose (float): 多巴酚丁胺剂量（mcg/kg/min）\n        - epinephrine_dose (float): 肾上腺素剂量（mcg/kg/min）\n        - norepinephrine_dose (float): 去甲肾上腺素剂量（mcg/kg/min）\n    returns: cardiovascular_score (int): 心血管系统得分（0-4分）\n    category: ConditionEvaluation\n    '''\n\n    # 条件1: 无低血压（MAP≥70且无血管活性药物）=0分\n    if map >= 70 and dopamine_dose == 0 and dobutamine_dose == 0 and epinephrine_dose == 0 and norepinephrine_dose == 0:\n        return 0\n    \n    # 条件2: MAP<70 mmHg=1分\n    if map < 70:\n        return 1\n    \n    # 条件3: 多巴胺≤5或任何剂量的多巴酚丁胺=2分\n    if dopamine_dose <= 5 or dobutamine_dose > 0:\n        return 2\n    \n    # 条件4: 多巴胺>5或肾上腺素≤0.1或去甲肾上腺素≤0.1=3分\n    if dopamine_dose > 5 or epinephrine_dose <= 0.1 or norepinephrine_dose <= 0.1:\n        return 3\n    \n    # 条件5: 多巴胺>15或肾上腺素>0.1或去甲肾上腺素>0.1=4分\n    if dopamine_dose > 15 or epinephrine_dose > 0.1 or norepinephrine_dose > 0.1:\n        return 4\n    \n    # 默认情况（理论上不会到达这里，但为了完整性）\n    return 0"
        },
        {
            "step_id": 6,
            "step_name": "Renal_score",
            "step_description": "根据肌酐水平或尿量计算肾脏系统得分",
            "step_inputs": [
                {
                    "input_name": "creatinine",
                    "input_desc": "肌酐水平（mg/dL）",
                    "input_type": "number",
                    "input_source": "$|inputs|.creatinine"
                },
                {
                    "input_name": "urine_output",
                    "input_desc": "尿量（mL/day）",
                    "input_type": "number",
                    "input_source": "$|inputs|.urine_output"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "renal_score",
                    "output_desc": "肾脏系统得分（0-4分）",
                    "output_type": "number"
                }
            ],
            "category": "ConditionEvaluation",
            "detail": "根据肌酐水平或尿量进行评估：1. 肌酐<1.2=0分；2. 肌酐1.2-1.9=1分；3. 肌酐2.0-3.4=2分；4. 肌酐3.5-4.9或尿量<500 mL/day=3分；5. 肌酐≥5.0或尿量<200 mL/day=4分。优先使用肌酐值，但当肌酐在临界范围时，尿量可能影响评分。",
            "code": "def renal_score(creatinine: float, urine_output: float) -> int:\n    '''\n    desc: 根据肌酐水平或尿量计算肾脏系统得分（0-4分）\n    args:\n        - creatinine (float): 肌酐水平（mg/dL）\n        - urine_output (float): 尿量（mL/day）\n    returns: renal_score: 肾脏系统得分（0-4分）\n    category: ConditionEvaluation\n    '''\n\n    if creatinine < 1.2:\n        renal_score = 0\n    elif 1.2 <= creatinine <= 1.9:\n        renal_score = 1\n    elif 2.0 <= creatinine <= 3.4:\n        renal_score = 2\n    elif 3.5 <= creatinine <= 4.9 or urine_output < 500:\n        renal_score = 3\n    elif creatinine >= 5.0 or urine_output < 200:\n        renal_score = 4\n    else:\n        renal_score = 0  # 默认情况，理论上不会到达\n\n    return renal_score"
        },
        {
            "step_id": 7,
            "step_name": "SOFA_total_score",
            "step_description": "计算SOFA总分",
            "step_inputs": [
                {
                    "input_name": "respiratory_score",
                    "input_desc": "呼吸系统得分",
                    "input_type": "number",
                    "input_source": "$|1|.respiratory_score"
                },
                {
                    "input_name": "platelets_score",
                    "input_desc": "血小板得分",
                    "input_type": "number",
                    "input_source": "$|2|.platelets_score"
                },
                {
                    "input_name": "gcs_score",
                    "input_desc": "神经系统得分",
                    "input_type": "number",
                    "input_source": "$|3|.gcs_score"
                },
                {
                    "input_name": "bilirubin_score",
                    "input_desc": "肝脏系统得分",
                    "input_type": "number",
                    "input_source": "$|4|.bilirubin_score"
                },
                {
                    "input_name": "cardiovascular_score",
                    "input_desc": "心血管系统得分",
                    "input_type": "number",
                    "input_source": "$|5|.cardiovascular_score"
                },
                {
                    "input_name": "renal_score",
                    "input_desc": "肾脏系统得分",
                    "input_type": "number",
                    "input_source": "$|6|.renal_score"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "sofa_total_score",
                    "output_desc": "SOFA总分（0-24分）",
                    "output_type": "number"
                }
            ],
            "category": "StatisticalAggregation",
            "detail": "将六个器官系统的得分相加：sofa_total_score = respiratory_score + platelets_score + gcs_score + bilirubin_score + cardiovascular_score + renal_score",
            "code": "def calculate_sofa_total_score(respiratory_score: float, platelets_score: float, gcs_score: float, bilirubin_score: float, cardiovascular_score: float, renal_score: float) -> float:\n    '''\n    desc: 计算SOFA总分，通过将六个器官系统的得分相加得到\n    args:\n        - respiratory_score (float): 呼吸系统得分\n        - platelets_score (float): 血小板得分\n        - gcs_score (float): 神经系统得分\n        - bilirubin_score (float): 肝脏系统得分\n        - cardiovascular_score (float): 心血管系统得分\n        - renal_score (float): 肾脏系统得分\n    returns: sofa_total_score: SOFA总分（0-24分）\n    category: StatisticalAggregation\n    '''\n\n    sofa_total_score = respiratory_score + platelets_score + gcs_score + bilirubin_score + cardiovascular_score + renal_score\n\n    return sofa_total_score"
        }
    ],
    "output": {
        "output_name": "sofa_total_score",
        "output_desc": "SOFA总分（0-24分），分数越高表示器官衰竭越严重",
        "output_type": "integer",
        "output_source": "$|7|.sofa_total_score"
    }
}


输入示例：

input_data = {
    "pao2_fio2_ratio": 350,
    "respiratory_support": False,
    "platelets": 120,
    "gcs": 14,
    "bilirubin": 1.5,
    "map": 80,
    "dopamine_dose": 0,
    "dobutamine_dose": 0,
    "epinephrine_dose": 0,
    "norepinephrine_dose": 0,
    "creatinine": 1.0,
    "urine_output": 1000
}
"""

import datetime
import json
import math


class CalculateFlow:
    def __init__(self, flow_definition):
        self.flow_definition = flow_definition

    # ============================================================
    # 子步骤 1：解析输入
    # ============================================================
    def _parse_inputs_for_step(self, step, context):
        input_params = {}

        for input_def in step['step_inputs']:
            input_source = input_def['input_source']
            if input_source is None: # 说明这个参数不需要从外部输入
                continue

            # 来源：inputs
            if input_source.startswith('$|inputs|.'):
                field = input_source.split('.')[-1]
                if field not in context['inputs']:
                    raise RuntimeError(
                        f"执行到步骤 {step['step_id']} 时，发现字段不存在: inputs.{field}"
                    )
                value = context['inputs'][field]

            # 来源：其它步骤
            elif input_source.startswith('$|'):
                ref_step_id = int(input_source.split('|')[1])
                ref_field = input_source.split('.')[-1]
                ref_key = f"step|{ref_step_id}|"

                if ref_field not in context.get(ref_key, {}):
                    print(f"context: \n{context}")
                    raise RuntimeError(
                        f"执行到步骤{step['step_id']}时，发现字段不存在: {ref_key}.{ref_field}"
                    )
                value = context[ref_key][ref_field]

            else:
                raise ValueError(f"Invalid input source: {input_source}")

            input_params[input_def['input_name']] = value

        return input_params

    # ============================================================
    # 子步骤 2：编译并执行 code
    # ============================================================
    def _compile_and_exec_code(self, step, input_params):
        try:
            safe_globals = {
                '__builtins__': __builtins__,
                'datetime': datetime,
                'math': math,
                'json': json,
            }
            safe_locals = {}

            # 执行 code
            exec(step['code'], safe_globals, safe_locals)
            func_name = None
            for name, obj in safe_locals.items():
                print(name, obj)
                if callable(obj):
                    func_name = name
                    break

            # 约定：函数名必须是 step_function
            # if 'step_function' not in safe_locals:
            #     raise RuntimeError("code must define a 'step_function'")

            # 调用
            print("func_name:", func_name)
            return safe_locals[func_name](**input_params)

        except Exception as e:
            raise RuntimeError(f"执行步骤时出错: {str(e)}")

    # ============================================================
    # 子步骤 3：保存输出到 context
    # ============================================================
    def _store_step_output(self, step, step_key, output, context):
        # 若函数返回 dict，则将多个字段写入 context
        # 多个输出必须保证是 dict 形式
        if isinstance(output, dict):
            for k, v in output.items():
                context[step_key][k] = v
        else:
            # 单输出（保持你原始逻辑）
            output_name = step['step_outputs'][0]['output_name']
            context[step_key][output_name] = output

    # ============================================================
    # 主流程：calculate
    # ============================================================
    def calculate(self, inputs):
        context = {"inputs": inputs.copy()}

        # 按 step_id 顺序执行
        # for step in sorted(self.flow_definition['steps'], key=lambda x: int(x['step_id'])):
        for step in self.flow_definition['steps']:
            step_id = step['step_id']
            step_key = f"step|{step_id}|"
            context[step_key] = {}

            # --- 子步骤 1：解析输入 ---
            input_params = self._parse_inputs_for_step(step, context)

            # --- 子步骤 2：执行函数 ---
            output = self._compile_and_exec_code(step, input_params)

            # --- 子步骤 3：存储输出 ---
            self._store_step_output(step, step_key, output, context)

        # --- 最终输出解析 ---
        output_source = self.flow_definition['output']['output_source']
        step_id = int(output_source.split('|')[1])
        output_name = output_source.split('.')[-1]

        return context[f"step|{step_id}|"][output_name]


    # 辅助检验工具
    def _validate_inputs_for_step(self, step, context:dict):
        processed_context = {}
        for k, vlist in context.items():
            # print(f"k: {k}, vlist: {vlist}")
            item = list()
            for v in vlist:
                if "input_name" in v:
                    item.append(v["input_name"])
                else:
                    item.append(v["output_name"])
            processed_context[k] = item
        # input_params = {}
        print(f"processed_context: \n{processed_context}")
        print(f"step: \n{step}")
        for input_def in step['step_inputs']:
            input_source = input_def['input_source']
            if input_source is None: # 说明这个参数不需要从外部输入
                continue

            # 来源：inputs
            if input_source.startswith('$|inputs|.'):
                field = input_source.split('.')[-1]
                if field not in processed_context['inputs']:
                    # print(field)
                    # print(processed_context['inputs'])
                    raise RuntimeError(
                        f"检测到步骤 {step['step_id']} 时，发现字段不存在: inputs.{field}"
                    )
                # value = context['inputs'][field]

            # 来源：其它步骤
            elif input_source.startswith('$|'):
                ref_step_id = int(input_source.split('|')[1])
                ref_field = input_source.split('.')[-1]
                # ref_key = f"step|{ref_step_id}|"
                ref_key = str(ref_step_id)

                if ref_field not in processed_context.get(ref_key, []):
                    # print(processed_context)
                    print(ref_field)
                    print(processed_context.get(ref_key, []))
                    raise RuntimeError(
                        f"检测到步骤{step['step_id']}时，发现字段不存在: {ref_key}.{ref_field}"
                    )
                # value = context[ref_key][ref_field]

            else:
                raise ValueError(f"Invalid input source: {input_source}")

        return True

    def calculate_wo_code_exec(self, inputs):
        """
        让模型参照 rule 的定义自己对输入参数进行计算
        """
        pass