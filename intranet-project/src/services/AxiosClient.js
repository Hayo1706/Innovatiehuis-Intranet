import axios from 'axios';
const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api'

});

axiosClient.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `Bearer ${token}` : '';
    return config;
});
export default axiosClient

