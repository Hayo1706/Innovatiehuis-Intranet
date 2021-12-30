
import axios from 'axios';
import router from '../main';

const axiosClient = axios.create({
    baseURL: 'http://localhost:8080/api' //TODO Change when in production

});


axiosClient.interceptors.response.use(response => {

    return response
},
    err => {

        //login error
        if (err.response.status == 401) {
            localStorage.removeItem("loggedIn");
            router.push('/login');

        }
    }

);
export default axiosClient

