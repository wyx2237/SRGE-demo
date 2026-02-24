<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 左侧品牌区域 -->
      <div class="brand-side">
        <!-- 装饰背景圆环 -->
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        
        <div class="brand-content">
          <div class="logo-text">SRGE</div>
          <div class="brand-divider"></div>
          <div class="brand-desc">
            Intelligent Workflow-based <br>
            Structured Rule Generation System
          </div>
          
          <div class="feature-tags">
            <div class="feature-item">
              <el-icon><Monitor /></el-icon>
              <span>Auto Medical Calculation</span>
            </div>
            <div class="feature-item">
              <el-icon><Cpu /></el-icon>
              <span>Structured Rule Generation</span>
            </div>
            <div class="feature-item">
              <el-icon><Connection /></el-icon>
              <span>Case Management</span>
            </div>
          </div>
        </div>
        
        <div class="brand-footer">
          &copy; 2026 Anonymous Lab
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-side">
        <div class="form-header">
          <h2 class="title">Welcome Back</h2>
          <p class="subtitle">Enter your details to access your workspace</p>
        </div>

        <el-form 
          :model="form" 
          :rules="rules" 
          ref="formRef" 
          size="large" 
          class="login-form"
          @keyup.enter="submit"
        >
          <el-form-item prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="Username / Email" 
              :prefix-icon="User"
              class="custom-input"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input 
              v-model="form.password" 
              placeholder="Password" 
              show-password
              :prefix-icon="Lock"
              class="custom-input"
            />
          </el-form-item>

          <div class="form-actions">
            <el-checkbox v-model="remember" label="Remember me" />
            <el-link type="primary" :underline="false" class="forgot-link">Forgot Password?</el-link>
          </div>

          <el-button type="primary" class="submit-btn" :loading="loading" @click="submit" round>
            SIGN IN
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>

          <div class="demo-tips">
            <el-alert 
              title="Demo Account: doctor / doctor" 
              type="info" 
              :closable="false" 
              show-icon 
            />
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, ArrowRight, Monitor, Cpu, Connection } from '@element-plus/icons-vue'

defineOptions({ name: 'LoginView' })

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const remember = ref(true)

const form = reactive({
  username: 'doctor',
  password: 'doctor',
})

const rules: FormRules = {
  username: [{ required: true, message: 'Please enter username', trigger: 'blur' }],
  password: [{ required: true, message: 'Please enter password', trigger: 'blur' }],
}

const submit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 模拟 API 调用延迟
        await new Promise(resolve => setTimeout(resolve, 800))
        localStorage.setItem('token', 'demo-token-v2')
        await router.replace('/dashboard')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped lang="scss">
/* 定义变量 - 方便微调颜色 */
$primary-color: #3b82f6; /* 核心蓝色 */
$accent-color: #06b6d4;  /* 辅助青色 */
$bg-gradient: linear-gradient(135deg, #f0f2f5 0%, #e1e6eb 100%);
$brand-gradient: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
$text-main: #1e293b;
$text-sub: #64748b;

.login-container {
  min-height: 100vh;
  background: $bg-gradient;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-box {
  width: 1000px;
  max-width: 100%;
  height: 600px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.05), 
    0 10px 10px -5px rgba(0, 0, 0, 0.02),
    0 0 0 1px rgba(0,0,0,0.03); /* 细微边框 */
  display: flex;
  overflow: hidden;
  position: relative;
  
  /* 入场动画 */
  animation: fadeUp 0.6s ease-out;
}

/* --- 左侧品牌区域 --- */
.brand-side {
  flex: 1.1; /* 占比略大 */
  background: $brand-gradient;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 60px;
  color: white;
  overflow: hidden;
  
  .brand-content {
    position: relative;
    z-index: 10;
  }
}

.logo-text {
  font-size: 48px;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(to right, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-divider {
  width: 40px;
  height: 4px;
  background: $accent-color;
  margin: 20px 0;
  border-radius: 2px;
}

.brand-desc {
  font-size: 18px;
  line-height: 1.6;
  color: #cbd5e1;
  font-weight: 300;
}

.feature-tags {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  
  .feature-item {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #e2e8f0;
    
    .el-icon {
      background: rgba(255, 255, 255, 0.1);
      padding: 8px;
      border-radius: 8px;
      font-size: 18px;
      color: $accent-color;
    }
  }
}

.brand-footer {
  position: relative;
  z-index: 10;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
}

/* 装饰圆环 */
.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, $accent-color, transparent);
  opacity: 0.1;
  filter: blur(40px);
}
.circle-1 {
  width: 300px;
  height: 300px;
  top: -50px;
  right: -50px;
}
.circle-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  background: linear-gradient(135deg, $primary-color, transparent);
}

/* --- 右侧表单区域 --- */
.form-side {
  flex: 1;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #fff;
}

.form-header {
  margin-bottom: 32px;
  .title {
    font-size: 28px;
    font-weight: 700;
    color: $text-main;
    margin: 0 0 8px;
  }
  .subtitle {
    font-size: 14px;
    color: $text-sub;
    margin: 0;
  }
}

/* 覆盖 Element 输入框样式 */
.custom-input {
  :deep(.el-input__wrapper) {
    box-shadow: none;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    transition: all 0.3s;
    padding: 8px 15px;
    
    &.is-focus {
      background: #fff;
      border-color: $primary-color;
      box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    }
  }
  
  :deep(.el-input__inner) {
    height: 36px; // 实际输入区域高度
  }
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  
  :deep(.el-checkbox__label) {
    color: $text-sub;
  }
  
  .forgot-link {
    font-size: 14px;
    color: $primary-color;
    &:hover {
      color: darken($primary-color, 10%);
    }
  }
}

.submit-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  background: linear-gradient(to right, $primary-color, darken($primary-color, 5%));
  border: none;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    background: linear-gradient(to right, darken($primary-color, 5%), darken($primary-color, 10%));
  }
  
  &:active {
    transform: translateY(0);
  }
}

.demo-tips {
  margin-top: 30px;
  :deep(.el-alert) {
    border-radius: 8px;
    background-color: #f0f9ff;
    color: $text-sub;
    border: 1px dashed #bae6fd;
    .el-alert__title {
        font-weight: 600;
    }
    .el-alert__icon {
        color: $primary-color;
    }
  }
}

/* 响应式适配 */
@media (max-width: 960px) {
  .login-box {
    flex-direction: column;
    height: auto;
    width: 500px;
  }
  
  .brand-side {
    padding: 40px;
    min-height: 200px;
    
    .brand-desc, .feature-tags, .brand-divider, .brand-footer {
      display: none; // 移动端简化显示
    }
    .logo-text {
      font-size: 32px;
      text-align: center;
    }
  }
  
  .form-side {
    padding: 40px;
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>