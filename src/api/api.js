import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8080', // 确保指向后端服务
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json', // 指定以 JSON 格式发送
  },
});

export default api;
