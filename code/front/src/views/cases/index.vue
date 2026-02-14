<template>
  <div class="case-library-page">
    <!-- 头部：标题与搜索 -->
    <div class="page-header">
      <div>
        <h2><el-icon><Collection /></el-icon> 案例库 (Case Library)</h2>
        <p class="subtitle">包含典型临床计算场景的标准输入与参考结果，用于演示与验证。</p>
      </div>
      <div class="actions">
        <el-input 
          v-model="searchKeyword" 
          placeholder="搜索问题或标签..." 
          prefix-icon="Search"
          style="width: 300px;" 
          clearable
        />
      </div>
    </div>

    <!-- 核心列表 -->
    <el-card shadow="never" class="table-card">
      <el-table :data="filteredCases" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" sortable />
        
        <el-table-column prop="question" label="计算问题 (Question)" min-width="200">
          <template #default="{ row }">
            <span class="question-text">{{ row.question }}</span>
          </template>
        </el-table-column>

        <el-table-column label="包含数据" width="180">
          <template #default>
            <el-tag size="small" type="info">Formula</el-tag>
            <el-tag size="small" type="info" style="margin-left: 5px">Context</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="result" label="参考结果" width="180">
          <template #default="{ row }">
            <span class="result-highlight">{{ row.result }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openDetails(row)">查看详情</el-button>
            <el-button size="small" type="primary" plain icon="VideoPlay" @click="runCase(row)">
              去计算
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 详情抽屉 (Drawer) -->
    <el-drawer
      v-model="drawerVisible"
      title="案例详情"
      direction="rtl"
      size="50%"
    >
      <div v-if="currentCase" class="case-detail">
        
        <!-- 1. 输入数据区域 -->
        <el-divider content-position="left">
          <el-icon><EditPen /></el-icon> 输入数据 (Input Data)
        </el-divider>

        <div class="detail-block">
          <h4>Question</h4>
          <div class="text-box">{{ currentCase.question }}</div>
        </div>

        <div class="detail-block">
          <h4>Formula / Logic</h4>
          <div class="code-box">{{ currentCase.formula }}</div>
        </div>

        <div class="detail-block">
          <h4>Clinical Text (脱敏)</h4>
          <div class="text-box context-bg">{{ currentCase.clinicalText }}</div>
        </div>

        <!-- 2. 结果数据区域 -->
        <el-divider content-position="left">
          <el-icon><DataAnalysis /></el-icon> 结果数据 (Result Data)
        </el-divider>

        <div class="detail-block">
          <h4>Medical Calculation Process (过程解释)</h4>
          <el-alert :closable="false" type="success">
            <div class="process-text" v-html="currentCase.explanation"></div>
          </el-alert>
        </div>

        <div class="detail-block">
          <h4>Final Result</h4>
          <div class="final-result-box">
            {{ currentCase.result }}
          </div>
        </div>
      </div>
      
      <template #footer>
        <div style="flex: auto">
          <el-button @click="drawerVisible = false">关闭</el-button>
          <el-button type="primary" @click="runCase(currentCase!)">
            使用此案例执行计算
          </el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Collection, Search, VideoPlay, EditPen, DataAnalysis } from '@element-plus/icons-vue';

// 1. 类型定义
interface CaseItem {
  id: number;
  question: string;
  formula: string;
  clinicalText: string;
  explanation: string;
  result: string;
}

// 2. 模拟数据 (Mock Data)
const mockData: CaseItem[] = [
  {
    id: 101,
    question: "计算身体质量指数 (BMI)",
    formula: "BMI = weight_kg / (height_m * height_m)",
    clinicalText: "患者张三，男性，45岁。本次入院体检显示：身高178厘米，体重85公斤。血压120/80mmHg，心率72次/分。既往有高血压病史...",
    explanation: "1. 抽取参数 <b>weight_kg</b>: 85 (从 '体重85公斤');<br>2. 抽取参数 <b>height_m</b>: 1.78 (从 '身高178厘米' 自动换算);<br>3. 代入公式: 85 / (1.78 * 1.78);<br>4. 计算得出 26.827...",
    result: "26.83 kg/m²"
  },
  {
    id: 102,
    question: "估算肾小球滤过率 (eGFR - CKD-EPI)",
    formula: "若性别=男: 141 * min(Scr/0.9, 1)^(-0.411) * max(Scr/0.9, 1)^(-1.209) * 0.993^Age",
    clinicalText: "患者李四，男，62岁。实验室检查结果显示血肌酐(Scr)为 1.2 mg/dL。目前无透析史，状态稳定。",
    explanation: "1. 识别参数 <b>Gender</b>: Male;<br>2. 识别参数 <b>Age</b>: 62;<br>3. 识别参数 <b>Scr</b>: 1.2 mg/dL;<br>4. 应用男性公式分支计算...",
    result: "68.5 mL/min/1.73m²"
  },
  {
    id: 103,
    question: "CHA2DS2-VASc 房颤卒中风险评分",
    formula: "Score = CHF(1) + Hypertension(1) + Age>=75(2) + Diabetes(1) + Stroke(2) + Vascular(1) + Age65-74(1) + SexCat(1)",
    clinicalText: "70岁女性患者，既往有高血压病史10年，控制不佳。无糖尿病，无心衰病史。去年曾发生过一次短暂性脑缺血发作(TIA)。",
    explanation: "1. <b>Age</b> 70岁 (65-74区间): +1分<br>2. <b>Sex</b> Female: +1分<br>3. <b>Hypertension</b> (有高血压): +1分<br>4. <b>Stroke/TIA</b> (有TIA史): +2分<br>5. 其他项为0。",
    result: "5 分 (高风险)"
  }
];

// 3. 逻辑处理
const router = useRouter();
const searchKeyword = ref('');
const drawerVisible = ref(false);
const currentCase = ref<CaseItem | null>(null);

// 过滤逻辑
const filteredCases = computed(() => {
  if (!searchKeyword.value) return mockData;
  const k = searchKeyword.value.toLowerCase();
  return mockData.filter(item => 
    item.question.toLowerCase().includes(k) || 
    item.result.toLowerCase().includes(k)
  );
});

// 打开详情
const openDetails = (row: CaseItem) => {
  currentCase.value = row;
  drawerVisible.value = true;
};

// 跳转到计算页面并传参
const runCase = (row: CaseItem) => {
  router.push({
    path: '/calculation',
    query: {
      question: row.question,
      formula: row.formula,
      clinicalText: row.clinicalText
    }
  });
};
</script>

<style scoped lang="scss">
.case-library-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  
  h2 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 24px;
    color: var(--el-text-color-primary);
  }
  .subtitle {
    margin: 8px 0 0;
    color: var(--el-text-color-secondary);
    font-size: 14px;
  }
}

.table-card {
  border-radius: 12px;
}

.question-text {
  font-weight: 600;
  color: var(--el-text-color-regular);
}

.result-highlight {
  font-weight: bold;
  color: var(--el-color-success);
}

/* Drawer Styles */
.case-detail {
  padding: 0 10px;
}

.detail-block {
  margin-bottom: 24px;
  
  h4 {
    margin: 0 0 8px;
    color: var(--el-text-color-secondary);
    font-size: 13px;
    text-transform: uppercase;
  }
}

.text-box {
  background: var(--el-fill-color-light);
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
  
  &.context-bg {
    background: #ecf5ff; /* 浅蓝色背景突出临床文本 */
    border-left: 4px solid #409EFF;
  }
}

.code-box {
  background: #282c34;
  color: #abb2bf;
  padding: 12px;
  border-radius: 6px;
  font-family: 'Consolas', monospace;
  font-size: 13px;
}

.process-text {
  font-size: 14px;
  line-height: 1.8;
}

.final-result-box {
  font-size: 24px;
  font-weight: bold;
  color: #67C23A;
  border: 1px dashed #67C23A;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  background: #f0f9eb;
}
</style>