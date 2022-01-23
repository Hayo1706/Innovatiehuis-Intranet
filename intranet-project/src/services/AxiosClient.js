
import axios from 'axios';
import router from '../main';
import LoginService from "@/services/LoginService";
import AlertService from './AlertService';

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
    if (error.code == "ECONNABORTED"){
        return Promise.reject(error);
    }
    //catch login error
    if (error.response.status == 4010 && router.currentRoute.value.fullPath != '/login') {
        LoginService.logout();
        window.location.reload();
        console.log("User was logged out due to invalid or expired JSON Web Token.")
        AlertService.alert("Uw sessie is ongeldig of verlopen. Log opnieuw in om terug te keren naar de vorige pagina.", "error")
    }
    //catch users accessing pages they shouldn't, without letting them know the page exists
    if (error.response.status == 403) {
        router.push({path:"/404"});
    }
    return Promise.reject(error);
});


export default axiosClient

