import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var UserService = function () {


    async function getUsers() {
        const { data } = await axiosClient.get('/users', { timeout: 2000 });
        data.forEach(user => { user.created = jsonToJsDate(user.created) });
        data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
        });
        return data;
    }
    async function getUsersByProject(projectid) {

        const { data } = await axiosClient.get(`/projects/${projectid}/users`, { timeout: 2000 });
        data.forEach(user => { user.created = jsonToJsDate(user.created) });
        data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
        });
        return data;

    }
    async function getUserById(userid) {
        const { data } = await axiosClient.get(`/users/${userid}`, { timeout: 2000 });
        data.forEach(user => { user.created = jsonToJsDate(user.created) });
        data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
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
    async function addUserToProject(projectid, userid) {
        const { data } = await axiosClient.post(`/projects/${projectid}/users/${userid}`, { timeout: 2000 });
        return data;
    }
    async function removeUserFromProject(projectid, userid) {
        const { data } = await axiosClient.delete(`/projects/${projectid}/users/${userid}`, { timeout: 2000 });
        return data;
    }
    async function updateUser(user, userid) {
        const { data } = await axiosClient.put(`/users/${userid}`, user, { timeout: 2000 });
        return data;
    }
    async function updateUserRole(roleid, userid) {
        const { data } = await axiosClient.patch(`/users/${userid}/role/${roleid}`, { timeout: 2000 });
        return data;
    }
    async function updateUserScreening(screeningstatus, userid) {
        const { data } = await axiosClient.patch(`/users/${userid}/screening/${screeningstatus}`, { timeout: 2000 });
        return data;
    }
    async function getRoles() {
        const { data } = await axiosClient.get(`/roles`, { timeout: 2000 });
        return data;
    }
    return {
        getUsers,
        getUserById,
        addUser,
        deleteUser,
        updateUser,
        getUsersByProject,
        addUserToProject,
        removeUserFromProject,
        updateUserRole,
        updateUserScreening,
        getRoles
    }

}
export default UserService();
