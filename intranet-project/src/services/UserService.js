import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var UserService = function () {


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
    async function deleteUser(userid) {
        const { data } = await axiosClient.delete(`/users/${userid}`, { timeout: 2000 });
        return data;
    }
    return {
        getUsers,
        getUserById,
        deleteUser
    }

}
export default UserService();
