import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var UserService = function () {


    async function getUsers() {
        const { response } = await axiosClient.get('/users', { timeout: 2000 });
        response.data.forEach(user => { user.created = jsonToJsDate(user.created) });
        response.data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
        });
        return response;
    }
    async function getUsersByProject(projectid) {

        const { response } = await axiosClient.get(`/projects/${projectid}/users`, { timeout: 2000 });
        response.data.forEach(user => { user.created = jsonToJsDate(user.created) });
        response.data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
        });
        return response;

    }
    async function getUserById(userid) {
        const { response } = await axiosClient.get(`/users/${userid}`, { timeout: 2000 });
        response.data.forEach(user => { user.created = jsonToJsDate(user.created) });
        response.data.forEach(user => {
            user.last_seen = jsonToJsDate(user.last_seen)
        });
        return response;
    }
    async function deleteUser(userid) {
        const { response } = await axiosClient.delete(`/users/${userid}`, { timeout: 2000 });
        return response;
    }
    async function addUser(user) {
        const { response } = await axiosClient.post(`/users`, user, { timeout: 2000 });
        return response;
    }
    async function addUserToProject(projectid, userid) {
        const { response } = await axiosClient.post(`/projects/${projectid}/users/${userid}`, { timeout: 2000 });
        return response;
    }
    async function removeUserFromProject(projectid, userid) {
        const { response } = await axiosClient.delete(`/projects/${projectid}/users/${userid}`, { timeout: 2000 });
        return response;
    }
    async function updateUser(user, userid) {
        const { response } = await axiosClient.put(`/users/${userid}`, user, { timeout: 2000 });
        return response;
    }
    async function updateUserRole(roleid, userid) {
        const { response } = await axiosClient.patch(`/users/${userid}/role/${roleid}`, { timeout: 2000 });
        return response;
    }
    async function updateUserScreening(screeningstatus, userid) {
        const { response } = await axiosClient.patch(`/users/${userid}/screening/${screeningstatus}`, { timeout: 2000 });
        return response;
    }
    async function getRoles() {
        const { response } = await axiosClient.get(`/roles`, { timeout: 2000 });
        return response;
    }
    async function updateRole(role, roleid) {
        const { response } = await axiosClient.put(`/roles/${roleid}`, role,{ timeout: 2000 });
        return response;
    }
    async function addRole(role) {
        const { response } = await axiosClient.post(`/roles`, role,{ timeout: 2000 });
        return response;
    }
    async function deleteRole(roleid,password) {
        const { response } = await axiosClient.delete(`/roles/${roleid}`, { data: {password: password}, headers:{ timeout: 2000 }});
        return response;
    }
    return {
        getUsers,
        deleteRole,
        getUserById,
        addRole,
        addUser,
        deleteUser,
        updateRole,
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
