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

    function setJWT(data) {

        this.$cookies.set(key, value)
    }

    return {
        attemptLogin,
        setJWT
    }

}
export default LoginService();
