FormulaCalculation = { 
    "general": """
类别：FormulaCalculation
说明：公式计算类别，主要进行特定数学公式的计算，涉及精确复杂的数值计算
输入定义：输入应该是计算该公式所需的全部变量; 大多数情况下，每个输入参数都是一个单一元素；特殊情况下，每个输入参数需要作为list传入，必须保证每个list长度相同，其中元素按照顺序一一对应。
输出定义：输出参数应该是一个明确的单一变量，一般情况下是通用类型的变量（number / string / boolean）
在特定情形下允许dict / list / tuple 等复合类型
""",
    "code_logic":"""
类别：FormulaCalculation
核心代码逻辑：
1. 导入需要的计算库，比如math
2. 将公式字符串转变为python可执行的表达式并写在代码中，公式中的变量名称必须和输入参数完全一致
""",
}


{
    "general_info": {
        "Name": "FormulaCalculation",
        "Description": "Formula calculation category, primarily performing calculations for specific mathematical formulas, involving precise and complex numerical computations."
    },
    "flow_info": {
        "Input": "Input should include all variables required to calculate the formula; in most cases, each input parameter is a single element; in special cases, each input parameter needs to be passed as a list, ensuring that all lists have the same length, with elements corresponding one-to-one in order.",
        "Output": "The output parameter should be a clear single variable, typically of a general type (number/string/boolean); compound types such as dict/list/tuple are allowed in specific cases."
    },
    "code_info": {
        "Language": "python",
        "Library": "math",
        "Logic": "1. Import necessary calculation libraries, such as math.\n2. Convert formula strings into Python-executable expressions in the code, ensuring variable names in the formula exactly match the input parameters."
    }
}



ConditionEvaluation = {
    "general": """
类别：ConditionEvaluation
说明：条件判断类别，主要进行条件表达式的判断，输出预设的条件结果值（如 if gender == 'male' then 1 else 0）
输入定义：输入应为条件表达式所需判断的变量
输出定义：输出应参照具体定义，每个分支输出对应的结果值（可能是string / number / boolean）
""", 
    "code_logic":"""
类别：ConditionEvaluation
核心代码逻辑：按照条件分支简洁地实现，用if-else语句实现，每个条件分支返回对应的结果值。
"""
}

DiscreteValueMapping = {
    "general":"""
类别：DiscreteValueMapping
说明：离散值映射类别，将有限的输入值映射为预设的输出值，常用于状态码转换、分类标签映射等（如 {'A':1, 'B':2}）
输入定义：输入应为一个离散值（如数字、字符串或枚举值）；映射表字典应内置在代码中，不能作为输入参数传入
输出定义：输出为映射表中对应的值，类型可为任意通用类型或复合类型
""",
    "code_logic":"""
类别：DiscreteValueMapping
核心代码逻辑：根据输入参数的值，在映射表中查找对应的输出值，并返回。
"""
}

UnitConversion = {
    "general":"""
类别：UnitConversion
说明：单位转换类别，将某种单位的数值转换为另一种单位的等效数值（如 m → inches）
输入定义：输入应为原始单位的数值；转换单位时的系数关系应该内置，而不是作为输入参数传入
输出定义：输出为目标单位转换后的数值，通常为数字类型
""",
    "code_logic":"""
类别：UnitConversion
核心代码逻辑：根据输入参数的单位，将数值转换为目标单位，并返回结果数值。
"""
}

StatisticalAggregation = {
    "general":"""
类别：StatisticalAggregation
说明：统计聚合类别，对一组数据进行统计计算，如求和、平均、加权平均、最大值、最小值等
输入定义：输入应为一组数据（通常为数值列表）。具体的聚合计算方法应内置，而不是作为输入参数传入
输出定义：输出为聚合后的统计结果，一般为数字类型，部分统计可能输出复合类型（如分位数列表）
""",
    "code_logic":"""
类别：StatisticalAggregation
核心代码逻辑：根据实际需要的聚合计算方法进行计算，尽量用简单的相加、求平均（或加权平均）、求最大最小值等方法。
"""
}

LogicalCombination = {
    "general":"""
类别：LogicalCombination
说明：逻辑组合类别，用于对多个布尔值进行组合判断，形成复合逻辑判断（如 a and b or c and not d）
输入定义：输入应为表达式所需的全部布尔值变量
输出定义：输出为布尔值（true / false），表示整体逻辑表达式的结果
""",
    "code_logic":"""
类别：LogicalCombination
核心代码逻辑：根据实际计算的布尔表达式，以python的布尔运算符实现该表达式，所有变量名必须和输入参数完全一致，然后返回计算结果
"""
}

TimeSeriesProcessing = {
    "general":"""
类别：TimeSeriesProcessing
说明：时间序列处理类别，用于对时间序列数据进行处理（时间相减，日期格式转换，日期加时间等）
输入定义：输入应为时间序列数据（统一用字符串类型表示）
输出定义：输出为处理后的时间序列数据，类型保持为字符串类型
""",
    "code_logic":"""
类别：TimeSeriesProcessing
核心代码逻辑：根据实际需要的时间序列处理方法，调用python的datetime库进行处理，例如strptime()，strftime()等。
"""
}

ThresholdMapping = {
    "general":"""
类别：ThresholdMapping
说明：阈值映射类别，将输入值映射到预设的输出值，将连续的输出值通过多个阈值条件映射到不同的输出值
输入定义：输入应为一个在连续值域上的数值，以及一组阈值条件设置，如 0-10 -> low, 10-20 -> medium, 20-30 -> high
输出定义：输出为映射表中对应的值，类型可为任意通用类型或复合类型
""",
    "code_logic":"""
类别：ThresholdMapping
核心代码逻辑：根据输入参数的阈值，将输入参数映射到输出参数的不同区间，并返回映射结果，从输入参数的最高设定阈值开始判断。每个条件分支处用注释写明相关的判断逻辑。
"""
}


CategoryDict = {
    "FormulaCalculation":FormulaCalculation,
    "ConditionEvaluation":ConditionEvaluation,
    "DiscreteValueMapping":DiscreteValueMapping,
    "UnitConversion":UnitConversion,
    "StatisticalAggregation":StatisticalAggregation,
    "LogicalCombination":LogicalCombination,
    "TimeSeriesProcessing":TimeSeriesProcessing,
    "ThresholdMapping":ThresholdMapping,
}

