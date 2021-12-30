
import axios from 'axios';
import router from '../main';

const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api'

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

