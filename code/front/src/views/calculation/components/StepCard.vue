<template>
    <div class="step-card">
        <!-- 1. Header: Clean, only ID and Name -->
        <div class="step-header">
            <div class="step-title-group">
                <span class="step-number">#{{ step.step_id }}</span>
                <span class="step-name">{{ step.step_name }}</span>
            </div>
        </div>

        <div class="step-body">

            <!-- 2. Description -->
            <div class="step-desc">
                {{ step.step_description }}
            </div>

            <!-- 3. Data Flow Section (With Overlap Protection) -->
            <div class="data-flow-section">
                <!-- Inputs Column -->
                <div class="flow-col">
                    <div class="flow-header input-header">
                        <el-icon>
                            <BottomRight />
                        </el-icon> Inputs
                    </div>
                    <div v-if="step.step_inputs.length > 0" class="flow-list">
                        <div v-for="(input, idx) in step.step_inputs" :key="idx" class="var-item">
                            <div class="var-row-top">
                                <span class="var-name" :title="input.input_name">{{ input.input_name }}</span>
                                <span class="var-type">{{ input.input_type }}</span>
                            </div>
                            <div class="var-row-bottom">
                                <span class="var-desc" :title="input.input_desc">{{ input.input_desc }}</span>
                                <!-- <span class="var-source" :title="input.input_source">Src: {{ input.input_source}}</span> -->
                                <!-- <el-tooltip :content="input.input_desc" placement="top" effect="dark" :show-after="500">
                                    <el-icon class="info-icon">
                                        <InfoFilled />
                                    </el-icon>
                                </el-tooltip> -->
                            </div>
                        </div>
                    </div>
                    <div v-else class="empty-flow">No Inputs</div>
                </div>

                <!-- Divider Arrow -->
                <div class="flow-divider">
                    <el-icon>
                        <Right />
                    </el-icon>
                </div>

                <!-- Outputs Column -->
                <div class="flow-col">
                    <div class="flow-header output-header">
                        <el-icon>
                            <TopRight />
                        </el-icon> Outputs
                    </div>
                    <div v-if="step.step_outputs.length > 0" class="flow-list">
                        <div v-for="(output, idx) in step.step_outputs" :key="idx" class="var-item">
                            <div class="var-row-top">
                                <span class="var-name output" :title="output.output_name">{{ output.output_name
                                    }}</span>
                                <span class="var-type">{{ output.output_type }}</span>
                            </div>
                            <div class="var-row-bottom">
                                <span class="var-desc" :title="output.output_desc">{{ output.output_desc }}</span>
                            </div>
                        </div>
                    </div>
                    <div v-else class="empty-flow">No Outputs</div>
                </div>
            </div>

            <!-- 4. Step Info Box (Category + Reason + Detail Merged) -->
            <div class="step-info-box">

                <!-- Row 1: Category (Moved here) -->
                <div class="info-row">
                    <div class="i-label">
                        <el-icon>
                            <Menu />
                        </el-icon> Tool Category
                    </div>
                    <div class="i-value">
                        <el-tag :color="getCategoryColor(step.category)" effect="dark" size="small"
                            class="category-badge">
                            {{ step.category }}
                        </el-tag>
                    </div>
                </div>

                <!-- Row 2: Reason -->
                <div class="info-row">
                    <div class="i-label">
                        <el-icon>
                            <Aim />
                        </el-icon> Selection Reason
                    </div>
                    <div class="i-value text-content">{{ step.reason }}</div>
                </div>

                <!-- Row 3: Logic Detail -->
                <div class="info-row">
                    <div class="i-label">
                        <el-icon>
                            <Memo />
                        </el-icon> Logic Detail
                    </div>
                    <div class="i-value text-content code-style">{{ step.detail }}</div>
                </div>
            </div>

            <!-- 5. Python Code Implementation -->
            <div class="code-wrapper">
                <el-collapse class="code-collapse">
                    <el-collapse-item name="1">
                        <template #title>
                            <div class="code-collapse-header">
                                <div class="left">
                                    <el-icon>
                                        <Platform />
                                    </el-icon>
                                    <span>Python Implementation</span>
                                </div>
                                <span class="hint">Click to expand</span>
                            </div>
                        </template>
                        <div class="code-block">
                            <pre><code>{{ step.code }}</code></pre>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import {
    Aim, Platform, Memo, Menu,
    BottomRight, TopRight, Right, InfoFilled
} from '@element-plus/icons-vue';

// Define Props based on your JSON structure
interface StepInput {
    input_name: string;
    input_desc: string;
    input_type: string;
    input_source: string;
}

interface StepOutput {
    output_name: string;
    output_desc: string;
    output_type: string;
}

interface StepData {
    step_id: string;
    step_name: string;
    step_description: string;
    step_inputs: StepInput[];
    step_outputs: StepOutput[];
    category: string;
    reason: string;
    detail: string;
    code: string;
}

defineProps<{
    step: StepData
}>();

const getCategoryColor = (category: string) => {
    const map: Record<string, string> = {
        FormulaCalculation: '#3b82f6', // Blue
        DiscreteValueMapping: '#8b5cf6', // Purple
        ConditionEvaluation: '#f59e0b', // Orange
        Preprocessing: '#64748b', // Gray
        DataRetrieval: '#10b981' // Green
    };
    return map[category] || '#3b82f6';
};
</script>

<style scoped lang="scss">
.step-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.2s ease;
    margin-bottom: 10px;

    &:hover {
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }

    /* Header Styles */
    .step-header {
        background: #f8fafc;
        padding: 10px 20px;
        border-bottom: 1px solid #e2e8f0;

        .step-title-group {
            display: flex;
            align-items: center;
            gap: 10px;

            .step-number {
                font-family: 'Consolas', monospace;
                font-weight: 800;
                color: #94a3b8;
                font-size: 1.1rem;
                opacity: 0.5;
            }

            .step-name {
                font-weight: 700;
                color: #334155;
                font-size: 1rem;
                font-family: 'Consolas', monospace;
            }
        }
    }

    .step-body {
        padding: 20px;
    }

    /* Description */
    .step-desc {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* --- Data Flow Section --- */
    .data-flow-section {
        display: flex;
        align-items: stretch;
        background: #fdfdfd;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-bottom: 20px;
        position: relative;

        .flow-col {
            flex: 1;
            padding: 12px;
            min-width: 0;
            /* Crucial for preventing flex item overflow */

            .flow-header {
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                color: #94a3b8;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 6px;

                &.input-header {
                    color: #3b82f6;
                }

                &.output-header {
                    color: #10b981;
                }
            }

            .flow-list {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .empty-flow {
                font-size: 0.8rem;
                color: #cbd5e1;
                font-style: italic;
                padding: 4px;
            }
        }

        .flow-divider {
            width: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #cbd5e1;
            border-left: 1px dashed #e2e8f0;
            border-right: 1px dashed #e2e8f0;
            background: #fafafa;
        }

        /* Variable Item Style - Fixed Overlap */
        .var-item {
            background: #ffffff;
            border: 1px solid #f1f5f9;
            border-radius: 6px;
            padding: 8px 10px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);

            .var-row-top {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 4px;
                gap: 8px;

                .var-name {
                    font-family: 'Consolas', monospace;
                    font-weight: 700;
                    font-size: 0.85rem;
                    color: #334155;
                    background: #f1f5f9;
                    padding: 2px 6px;
                    border-radius: 4px;
                    /* Truncation */
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    min-width: 0;
                    /* flex shrink */

                    &.output {
                        color: #059669;
                        background: #ecfdf5;
                    }
                }

                .var-type {
                    font-size: 0.7rem;
                    color: #94a3b8;
                    background: #fff;
                    border: 1px solid #e2e8f0;
                    padding: 1px 6px;
                    border-radius: 10px;
                    flex-shrink: 0;
                    /* prevent shrinking */
                }
            }

            .var-row-bottom {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.75rem;
                color: #64748b;
                gap: 8px;

                .var-source,
                .var-desc {
                    font-family: 'Consolas', monospace;
                    color: #94a3b8;
                    /* Truncation logic */
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    min-width: 0;
                    flex: 1;
                }

                /* Make output description italic instead of monospace source */
                .var-desc {
                    font-family: sans-serif;
                    font-style: italic;
                }

                .info-icon {
                    flex-shrink: 0;
                    cursor: help;
                    color: #bfdbfe;

                    &:hover {
                        color: #3b82f6;
                    }
                }
            }
        }
    }

    /* --- Step Info Box (Category + Reason + Logic) --- */
    .step-info-box {
        background: #f8fafc;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;

        .info-row {
            display: flex;
            gap: 12px;
            margin-bottom: 12px;

            &:last-child {
                margin-bottom: 0;
            }

            .i-label {
                min-width: 140px;
                /* Fixed width for labels */
                color: #94a3b8;
                font-weight: 600;
                display: flex;
                align-items: flex-start;
                /* Top align for long text */
                gap: 6px;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 3px;
                /* visual alignment with text */
                flex-shrink: 0;
            }

            .i-value {
                color: #334155;
                font-size: 0.9rem;
                line-height: 1.6;
                flex: 1;
                word-break: break-word;
                /* Prevent overflow of long words */

                &.text-content {
                    /* specific logic text style */
                }

                &.code-style {
                    font-family: 'Consolas', monospace;
                    background: #ffffff;
                    border: 1px solid #f1f5f9;
                    padding: 4px 8px;
                    border-radius: 4px;
                    color: #475569;
                    font-size: 0.85rem;
                }

                .category-badge {
                    border: none;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                }
            }
        }
    }

    /* Code Block */
    .code-wrapper {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }

    .code-collapse {
        border: none;

        :deep(.el-collapse-item__header) {
            height: 36px;
            background-color: #f1f5f9;
            padding: 0 12px;
            border-bottom: 1px solid #e2e8f0;

            &.is-active {
                border-bottom-color: transparent;
            }
        }

        :deep(.el-collapse-item__arrow) {
            margin: 0;
            color: #94a3b8;
        }

        :deep(.el-collapse-item__content) {
            padding: 0;
        }

        .code-collapse-header {
            flex: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;

            .left {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.8rem;
                font-weight: 600;
                color: #64748b;
            }

            .hint {
                font-size: 0.75rem;
                color: #94a3b8;
                margin-right: 12px;
            }
        }

        .code-block {
            background: #1e293b;
            padding: 16px;
            overflow-x: auto;

            pre {
                margin: 0;
            }

            code {
                font-family: 'Consolas', monospace;
                color: #e2e8f0;
                font-size: 0.85rem;
                line-height: 1.6;
            }
        }
    }
}
</style>