import axiosClient from './AxiosClient';

var LoginService = function () {

    async function attemptLogin(loginAttempt) {
        return await axiosClient.post(`/auth`, loginAttempt, { timeout: 2000 }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
    }

    async function changePassword(loginAttempt,token) {
        return await axiosClient.put(`/auth/password?resettoken=` + token, loginAttempt, { timeout: 2000 }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
    }

    async function logout() {
        localStorage.clear();
        return await axiosClient.post('/auth/logout', null, { timeout: 2000 });
    }

    return {
        attemptLogin,
        changePassword,
        logout
    }
}
export default LoginService();
