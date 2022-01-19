
import axios from 'axios';
import router from '../main';
import LoginService from "@/services/LoginService";

const axiosClient = axios.create({
    baseURL: 'http://localhost:8080/api' //TODO Change when in production

});

axiosClient.interceptors.request.use(
    function (config) {
        config.headers["X-CSRF-TOKEN"] = document.cookie.match('(^|;)\\s*' + 'csrf_access_token' + '\\s*=\\s*([^;]+)')?.pop();
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

axiosClient.interceptors.response.use((config) => {
    return config;
}, (error) => {

    //login error
    if (error.response.status == 401 && router.currentRoute.value.fullPath != '/login') {
        LoginService.logout();
        window.location.reload();
    }
    if (error.response.status == 403) {
        router.push({path:"/404"});
    }
    
    return Promise.reject(error);
});


export default axiosClient

