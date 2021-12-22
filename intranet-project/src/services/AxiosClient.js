
import axios from 'axios';
import router from '../main';

const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api'

});

axiosClient.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `Bearer ${token}` : '';
    return config;
});
axiosClient.interceptors.response.use(response => {

    return response
},
    err => {

        //login error
        if (err.response.data.status == 401) {
            router.push('/login');

        }

    }

);
export default axiosClient

