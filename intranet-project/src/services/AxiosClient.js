
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
},
    (error) => {
        //catch timeout error
        if (error.code == "ECONNABORTED") {
            return Promise.reject(error);
        }
        //catch login error
        if (error.response.status == 401 && !router.currentRoute.value.fullPath.includes('/login')) {
            LoginService.logout();
            window.location.reload();
        }
        //catch users accessing pages they shouldn't, without letting them know the page exists
        if (error.response.status == 403) {
            if (localStorage.getItem("access_status") == 0) {
                router.push({ path: "/no_access" });
            } else {
                router.push({ path: "/404" });
            }

        }
        return Promise.reject(error);
    });


export default axiosClient

