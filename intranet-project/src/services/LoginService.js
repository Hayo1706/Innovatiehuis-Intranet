import axiosClient from './AxiosClient';

var LoginService = function () {


    async function attemptLogin(loginAttempt) {
        return await axiosClient.post(`/auth`, loginAttempt, { timeout: 2000 }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
    }

    async function logout() {
        localStorage.clear();
        return await axiosClient.post('/logout', null, { timeout: 2000 });
    }

    return {
        attemptLogin,
        logout
    }

}
export default LoginService();
