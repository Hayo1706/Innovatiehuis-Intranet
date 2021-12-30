import axiosClient from './AxiosClient';

var LoginService = function () {


    async function attemptLogin(loginAttempt) {
        return await axiosClient.post(`/auth`, loginAttempt, {timeout: 2000}, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
    }

    return {
        attemptLogin
    }

}
export default LoginService();
