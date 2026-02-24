import datetime
import json
import math

class CalculateFlow:
    def __init__(self, flow_definition):
        self.flow_definition = flow_definition

    # ... [之前的 _parse_inputs_for_step 保持不变] ...
    def _parse_inputs_for_step(self, step, context):
        input_params = {}
        for input_def in step['step_inputs']:
            input_source = input_def['input_source']
            if input_source is None: continue

            if input_source.startswith('$|inputs|.'):
                field = input_source.split('.')[-1]
                if field not in context['inputs']:
                    raise RuntimeError(f"Step {step['step_id']} missing input: {field}")
                value = context['inputs'][field]
            elif input_source.startswith('$|'):
                ref_step_id = int(input_source.split('|')[1])
                ref_field = input_source.split('.')[-1]
                ref_key = f"step|{ref_step_id}|"
                if ref_field not in context.get(ref_key, {}):
                    raise RuntimeError(f"Step {step['step_id']} missing dependency: {ref_key}.{ref_field}")
                value = context[ref_key][ref_field]
            else:
                raise ValueError(f"Invalid source: {input_source}")
            input_params[input_def['input_name']] = value
        return input_params

    # ... [之前的 _compile_and_exec_code 保持不变] ...
    def _compile_and_exec_code(self, step, input_params):
        try:
            safe_globals = {'__builtins__': __builtins__, 'datetime': datetime, 'math': math, 'json': json}
            safe_locals = {}
            exec(step['code'], safe_globals, safe_locals)
            func_name = None
            for name, obj in safe_locals.items():
                if callable(obj):
                    func_name = name
                    break
            return safe_locals[func_name](**input_params)
        except Exception as e:
            raise RuntimeError(f"Error in step {step['step_id']}: {str(e)}")

    # ... [之前的 _store_step_output 保持不变] ...
    def _store_step_output(self, step, step_key, output, context):
        if isinstance(output, dict):
            for k, v in output.items():
                context[step_key][k] = v
        else:
            output_name = step['step_outputs'][0]['output_name']
            context[step_key][output_name] = output

    # ============================================================
    # 核心修改：calculate 方法
    # ============================================================
    def calculate(self, inputs):
        context = {"inputs": inputs.copy()}
        
        # 1. 初始化结果列表
        execution_steps = []

        # 按 step_id 排序确保顺序正确
        sorted_steps = sorted(self.flow_definition['steps'], key=lambda x: int(x['step_id']))

        for step in sorted_steps:
            step_id = step['step_id']
            step_key = f"step|{step_id}|"
            detail = step['detail']
            context[step_key] = {}

            # --- 执行逻辑 ---
            input_params = self._parse_inputs_for_step(step, context)
            output_val = self._compile_and_exec_code(step, input_params)
            self._store_step_output(step, step_key, output_val, context)

            # --- 组装前端需要的 Trace 数据 ---
            
            # A. 构造 Logic 字符串 (显示为: "变量A=10, 变量B=True")
            # 这能让用户看到这一步是用什么数据算出来的
            logic_str = detail + " (" + ", ".join([f"{k}={v}" for k, v in input_params.items()]) + ")"
            if not logic_str:
                logic_str = step.get('detail', 'Calculation') # 如果没有输入参数，显示描述

            # B. 获取输出变量名和结果字符串
            if isinstance(output_val, dict):
                output_name = ", ".join(output_val.keys())
                result_str = json.dumps(output_val) # 复杂对象转JSON字符串
            else:
                output_name = step['step_outputs'][0]['output_name']
                if isinstance(output_val, float):
                    result_str = f"{output_val:.3f}"
                else:
                    result_str = str(output_val)

            # C. 构造单步对象 (样式全部使用默认值)
            trace_item = {
                "stepId": str(step_id),
                "stepName": step['step_name'],
                "category": step.get('category', 'Formula'),
                "logic": logic_str,             # 计算逻辑
                "outputName": output_name,      # 这一步输出的变量名
                "result": result_str,           # 这一步的计算结果
                
                # --- 样式默认值 ---
                "type": "primary",    # 默认蓝色
                "color": "",          # 留空，使用 type 的默认色
                "tagType": "info"     # 默认灰色标签
            }
            
            execution_steps.append(trace_item)

        # 获取最终计算结果值
        output_source = self.flow_definition['output']['output_source']
        final_step_id = int(output_source.split('|')[1])
        final_output_name = output_source.split('.')[-1]
        final_result = context[f"step|{final_step_id}|"][final_output_name]
        final_result = round(final_result, 3) if isinstance(final_result, float) else final_result


        # 返回包含结构化日志的字典
        # 对所有 float 类型数据进行处理，保留3位小数
        return {
            "final_result": final_result,
            "execution_steps": execution_steps
        }
    
    def _validate_inputs_for_step(self, step, context):
        # 检测当前步骤所有引用参数是否在上下文中已经存在
        print(f"context: {context}")
        # context_dict = {"inputs":[]}
        # for item in context["inputs"]:
        #     context_dict["inputs"].append(item["input_name"])


        for input_def in step['step_inputs']:
            input_source = input_def['input_source']
            if input_source is None: continue

            if input_source.startswith('$|inputs|.'):
                field = input_source.split('.')[-1]
                if field not in context['inputs']:
                    print(f"context['inputs']: {context['inputs']}")
                    raise RuntimeError(f"Step {step['step_id']} missing input: {field}")
            
            elif input_source.startswith('$|'):
                ref_step_id = input_source.split('|')[1] # str类型
                ref_field = input_source.split('.')[-1]
                ref_key = ref_step_id
                print(f"ref_key: {ref_key}")
                print(f"type of ref_key: {type(ref_key)}")
                print(f"ref_field: {ref_field}")
                if ref_field not in context.get(ref_key, {}):
                    print(f"context:{context}")
                    print(f"context[{ref_key}]: {context.get(ref_key, {})}")
                    raise RuntimeError(f"Step {step['step_id']} missing dependency: {ref_key}.{ref_field}")
