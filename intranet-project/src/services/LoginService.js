import axiosClient from './AxiosClient';

var LoginService = function () {


    async function attemptLogin(loginAttempt) {
        console.log(loginAttempt);
        const { data } = await axiosClient.post(`/auth`, { loginAttempt }, { timeout: 2000 }, {
            headers: {
                'Content-Type': 'plain/text'
            }
        });
        localStorage.setItem("token", data);
        return data;
    }

    return {
        attemptLogin
    }

}
export default LoginService();
