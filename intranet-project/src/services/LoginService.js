import axiosClient from './AxiosClient';

var LoginService = function () {


    async function attemptLogin(loginAttempt) {
        const { data } = await axiosClient.post(`/auth`, { loginAttempt }, { timeout: 2000, 'Content-Type': 'text/plain' },);
        localStorage.setItem("token", data);
        return data;
    }

    return {
        attemptLogin
    }

}
export default LoginService();
