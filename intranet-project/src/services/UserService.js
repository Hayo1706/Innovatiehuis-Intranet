import axios from 'axios';
import { jsonToJsDate } from './DataConverter';

var UserService = function () {
    const axiosClient = axios.create({
        baseURL: 'http://127.0.0.1:5000/api'
    });

    async function getUsers() {
        const { data } = await axiosClient.get('/users', { timeout: 2000 });
        data.forEach(user => { user.createdat = jsonToJsDate(user.createdat) });
        data.forEach(user => {
            user.lastseen = jsonToJsDate(user.lastseen)
        });
        return data;
    }
    async function getUserById(userid) {
        const { data } = await axiosClient.get(`'/users/${userid}`, { timeout: 2000 });
        data.forEach(user => { user.createdat = jsonToJsDate(user.createdat) });
        data.forEach(user => {
            user.lastseen = jsonToJsDate(user.lastseen)
        });
        return data;
    }

    return {
        getUsers,
        getUserById
    }

}
export default UserService();
