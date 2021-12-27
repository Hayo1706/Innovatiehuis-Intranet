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
    async function addUser(user) {
        const { data } = await axiosClient.post(`/users`, user, { timeout: 2000 });
        return data;
    }
    async function updateUser(user, userid) {
        const { data } = await axiosClient.put(`/users/${userid}`, user, { timeout: 2000 });
        return data;
    }
    return {
        getUsers,
        getUserById,
        addUser,
        deleteUser,
        updateUser
    }

}
export default UserService();
