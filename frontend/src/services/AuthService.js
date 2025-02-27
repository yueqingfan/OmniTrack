import axios from 'axios';

const API_URL = 'http://localhost:8080/api/users';  // 后端接口地址

const register = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, { username, password });
        return response;  // 返回整个响应对象
    } catch (error) {
        console.error("注册请求错误", error);
        throw error;  // 将错误抛出给调用者
    }
};

export default {
    register
};
