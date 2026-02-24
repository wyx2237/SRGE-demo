import axios, { type AxiosRequestConfig } from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_BASE_API,
  timeout: 300000
})

// 请求拦截器
// request.interceptors.request.use(config => {
//   const token = localStorage.getItem('token')
//   if (token) config.headers.Authorization = `Bearer ${token}`
//   return config
// })

// 响应拦截器
request.interceptors.response.use(
  res => res.data,
  error => {
    console.error('API Error:', error.message)
    return Promise.reject(error)
  }
)

export default request