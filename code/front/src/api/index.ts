import request from '@/utils/request'

// ============ 类型定义 ============
export interface LoginParams {
  username: string
  password: string
}

export interface UserInfo {
  id: number
  name: string
  email: string
}

export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

// ============ API 接口（全部集中在此）============
export const srge_api = {
  ruleGenerate: (data: {
    question: string,
    knowledge: string,
    text: string
  }) =>
    request.post('/rule/generate', data)
    .then(res => {
      console.log(res)
      const { structured_rule } = res.data
      return structured_rule
    })
    .catch(err => {
      console.error('Rule Generate Error:', err.message)
      return Promise.reject(err)
    }),

  calExec: (data: {
    rule: object,
    text: string
  }) =>
    request.post('/calculation/execute', data)
    .then(res => {
      console.log(res)
      const { input_source_list, execution_steps, final_result } = res.data
      return { input_source_list, execution_steps, final_result }
    })
    .catch(err => {
      console.error('Calculation Exec Error:', err.message)
      return Promise.reject(err)
    }),

  // // 用户相关
  // login: (data: LoginParams) => 
  //   request.post<ApiResponse<{ token: string }>>('/user/login', data),
  
  // getUserInfo: () => 
  //   request.get<ApiResponse<UserInfo>>('/user/info'),
  
  // logout: () => 
  //   request.post('/user/logout'),
  
  // // 订单相关
  // getOrderList: (params: { page: number; size: number }) => 
  //   request.get<ApiResponse<any[]>>('/order/list', { params }),
  
  // getOrderDetail: (id: number) => 
  //   request.get<ApiResponse<any>>(`/order/detail/${id}`),
  
  // createOrder: (data: any) => 
  //   request.post('/order/create', data),
  
  // // 产品相关
  // getProductList: (params?: any) => 
  //   request.get<ApiResponse<any[]>>('/product/list', { params }),
  
  // getProductDetail: (id: number) => 
  //   request.get<ApiResponse<any>>(`/product/detail/${id}`),
  
  // // 通用
  // uploadFile: (data: FormData) => 
  //   request.post('/upload', data, { headers: { 'Content-Type': 'multipart/form-data' } }),
  
  // getDashboard: () => 
  //   request.get<ApiResponse<any>>('/dashboard')
}