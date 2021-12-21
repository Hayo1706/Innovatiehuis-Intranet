import axios from 'axios';

var LoginService = function () {
    const axiosClient = axios.create({
        baseURL: 'http://127.0.0.1:5000/api'
    });

    async function attemptLogin(loginAttempt) {
        const { data } = await axiosClient.post(`/auth`, { loginAttempt }, { timeout: 2000 });
        return data;
    }

    return {
        attemptLogin
    }

}
export default LoginService();
