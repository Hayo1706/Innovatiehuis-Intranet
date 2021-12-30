import axiosClient from './AxiosClient';

var LoginService = function () {


    async function attemptLogin(loginAttempt) {
        const { data } = await axiosClient.post(`/auth`, loginAttempt, { timeout: 2000 }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        return data;
    }

    return {
        attemptLogin
    }

}
export default LoginService();
