<template>
  <div class="dashboard-container">
    <!-- 1. Hero Section: 核心视觉区 -->
    <div class="hero-section">
      <!-- Logo 区域：直接复用组件，开启 large 模式 -->
      <div class="system-branding">
        <Logo large />
      </div>

      <!-- 主标题 (无变化) -->
      <h1 class="hero-title">
        Structured Rule Generation<br />
        <span class="highlight">& Execution System</span>
      </h1>

      <!-- 副标题 (无变化) -->
      <p class="hero-subtitle">Supporting Clinical Medical Computation</p>

      <!-- 描述文案 -->
      <p class="hero-desc">
        Bridging the gap between unstructured EHR text and precise medical metrics. SRGE eliminates
        LLM inconsistency by transforming natural language requirements into deterministic,
        auditable, and interpretable computational workflows.
      </p>
      <p class="hero-desc hero-audience">
        This system is designed for <strong>clinicians and physicians</strong>. It helps doctors
        define, validate, and execute clinical rules in a transparent and auditable way, supporting
        evidence-based medical computation in daily practice.
      </p>

      <!-- 按钮组 (无变化) -->
      <div class="hero-actions">
        <el-button
          type="primary"
          size="large"
          round
          class="action-btn main-btn"
          @click="goToCalculation"
        >
          Start Medical Calculation <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
        <el-button size="large" round class="action-btn sec-btn" @click="goToDocumentation"> View Documentation </el-button>
      </div>
    </div>

    <!-- 2. Features Grid (无变化) -->
    <div class="features-grid">
      <!-- ... Feature Cards 内容保持不变 ... -->
      <div class="feature-card">
        <div class="icon-box blue">
          <el-icon><Menu /></el-icon>
        </div>
        <div class="card-content">
          <h3>Atomic Tool Library</h3>
          <p>
            A repository of standardized computational units (thresholds, logic ops) that ensures
            deterministic execution, eliminating the variability found in direct LLM reasoning.
          </p>
        </div>
      </div>
      <div class="feature-card">
        <div class="icon-box purple">
          <el-icon><MagicStick /></el-icon>
        </div>
        <div class="card-content">
          <h3>Rule Generation</h3>
          <p>
            Transforms natural language clinical requirements into structured, interpretable rule
            definitions, making the logic transparent and easy for experts to validate.
          </p>
        </div>
      </div>
      <div class="feature-card">
        <div class="icon-box green">
          <el-icon><VideoPlay /></el-icon>
        </div>
        <div class="card-content">
          <h3>Visual Execution Engine</h3>
          <p>
            A transparent workflow engine that records every state change and intermediate variable,
            providing full auditability and trust in critical medical decisions.
          </p>
        </div>
      </div>
    </div>

    <!-- 底部版权 (无变化) -->
    <div class="dashboard-footer">
      <span>SRGE v1.0.0</span>
      <span class="divider">|</span>
      <span>© 2026 ecustnlplab </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowRight, Menu, MagicStick, VideoPlay } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import Logo from '@/components/Logo.vue' // 引入组件

defineOptions({ name: 'DashboardView' })

const router = useRouter()

const goToCalculation = () => {
  router.push({ name: 'CalculationView' })
}

const goToDocumentation = () => {
  window.open('https://github.com/wyx2237/SRGE-demo', '_blank')
}
</script>

<style scoped lang="scss">
/* 全局容器 (无变化) */
.dashboard-container {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
  background-image:
    radial-gradient(
      at 0% 0%,
      color-mix(in srgb, var(--el-color-primary) 10%, transparent) 0px,
      transparent 50%
    ),
    radial-gradient(at 100% 0%, rgba(8, 145, 178, 0.05) 0px, transparent 50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 20px;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    sans-serif;
  box-sizing: border-box;
}

/* Dark mode: soften background glow */
:global(html.dark) .dashboard-container {
  background-image:
    radial-gradient(
      at 0% 0%,
      color-mix(in srgb, var(--el-color-primary) 16%, transparent) 0px,
      transparent 55%
    ),
    radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 55%);
}

/* --- 1. Hero Section --- */
.hero-section {
  text-align: center;
  max-width: 900px;
  margin-bottom: 90px;
  animation: fadeIn 0.8s ease-out;

  /* Logo 容器：只需简单定位即可，具体样式由组件内部控制 */
  .system-branding {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
    height: 80px; /* 显式占位，防止抖动 */
  }

  /* 标题样式 (无变化) */
  .hero-title {
    font-size: 3rem;
    line-height: 1.1;
    font-weight: 800;
    color: var(--el-text-color-primary);
    margin: 0 0 16px 0;
    letter-spacing: -1px;

    .highlight {
      background: -webkit-linear-gradient(120deg, #2563eb, #0891b2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .hero-subtitle {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--el-text-color-regular);
    margin: 0 0 24px 0;
    letter-spacing: -0.5px;
  }

  .hero-desc {
    font-size: 1.1rem;
    color: var(--el-text-color-secondary);
    line-height: 1.7;
    max-width: 760px;
    margin: 0 auto 48px auto;
  }

  .hero-audience {
    margin-top: -24px;
    margin-bottom: 48px;
    color: var(--el-text-color-regular);
  }

  .hero-actions {
    display: flex;
    justify-content: center;
    gap: 20px;

    .action-btn {
      font-weight: 600;
      padding: 24px 32px;
      font-size: 1rem;
      border-radius: 12px;
      transition:
        transform 0.2s,
        box-shadow 0.2s;

      &.main-btn {
        background-color: #0f172a;
        border-color: #0f172a;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2);

        &:hover {
          background-color: #1e293b;
          transform: translateY(-2px);
          box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.2);
        }
      }

      &.sec-btn {
        background-color: #fff;
        border: 1px solid #e2e8f0;
        color: #475569;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);

        &:hover {
          background-color: #f8fafc;
          border-color: #cbd5e1;
          color: #0f172a;
          transform: translateY(-2px);
        }
      }
    }
  }
}

/* --- 2. Features Grid (无变化) --- */
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1280px;
  width: 100%;
  padding: 0 20px;

  .feature-card {
    background: var(--el-bg-color);
    border-radius: 24px;
    padding: 40px 32px;
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.03),
      0 4px 10px -4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    animation: slideUp 0.8s ease-out;
    animation-fill-mode: both;
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    &:nth-child(1) {
      animation-delay: 0.1s;
    }
    &:nth-child(2) {
      animation-delay: 0.2s;
    }
    &:nth-child(3) {
      animation-delay: 0.3s;
    }

    &:hover {
      transform: translateY(-8px);
      box-shadow:
        0 0 0 1px rgba(37, 99, 235, 0.1),
        0 20px 25px -5px rgba(0, 0, 0, 0.05),
        0 8px 10px -6px rgba(0, 0, 0, 0.01);
    }

    .icon-box {
      width: 60px;
      height: 60px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      margin-bottom: 24px;
      transition: all 0.3s ease;
      &.blue {
        background: #eff6ff;
        color: #2563eb;
      }
      &.purple {
        background: #faf5ff;
        color: #9333ea;
      }
      &.green {
        background: #f0fdf4;
        color: #16a34a;
      }
    }

    &:hover .icon-box {
      transform: scale(1.1) rotate(5deg);
    }

    .card-content {
      h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--el-text-color-primary);
        margin: 0 0 12px 0;
        letter-spacing: -0.02em;
      }
      p {
        font-size: 0.95rem;
        color: var(--el-text-color-secondary);
        line-height: 1.65;
        margin: 0;
        text-align: left;
      }
    }
  }
}

/* --- 3. Footer (无变化) --- */
.dashboard-footer {
  margin-top: auto;
  padding-top: 100px;
  padding-bottom: 20px;
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 500;
  .divider {
    margin: 0 12px;
    color: #cbd5e1;
    opacity: 0.5;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.25rem;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
  .hero-actions {
    flex-direction: column;
  }
}
</style>
