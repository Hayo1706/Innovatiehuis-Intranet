import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var ProjectService = function () {


    async function getProjects() {
        const { data } = await axiosClient.get('/projects', { timeout: 2000 });
        data.forEach(project => { project.created = jsonToJsDate(project.created) });
        data.forEach(project => { project.last_updated = jsonToJsDate(project.last_updated) });
        return data;
    }
    async function getProjectById(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}`, { timeout: 2000 });
        data.forEach(project => { project.created = jsonToJsDate(project.created) });
        data.forEach(project => { project.last_updated = jsonToJsDate(project.last_updated) });
        return data;
    }
    async function deleteProject(id) {
        const { data } = await axiosClient.delete(`/projects/${id}`, { timeout: 2000 });
        return data;
    }
    async function archiveProject(project) {
        const { data } = await axiosClient.put(`/projects/${project.projectid}/archive`, { project }, { timeout: 2000 });
        return data;
    }
    async function getProjectsByUser(userid) {
        const { data } = await axiosClient.get(`/users/${userid}/projects`, { timeout: 2000 });
        data.forEach(project => { project.last_updated = jsonToJsDate(project.last_updated) });
        return data;
    }
    async function getParentsById(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/parents`, { timeout: 2000 });
        data.forEach(project => { project.created = jsonToJsDate(project.created) });
        data.forEach(project => { project.last_updated = jsonToJsDate(project.last_updated) });
        return data;
    }
    async function getChildrenById(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/children`, { timeout: 2000 });
        data.forEach(project => { project.created = jsonToJsDate(project.created) });
        data.forEach(project => { project.last_updated = jsonToJsDate(project.last_updated) });
        return data;
    }
    async function addProject(project) {
        const { data } = await axiosClient.post(`/projects`, { project }, { timeout: 2000 });
        return data;
    }
    async function updateProjectNameDescription(id, project) {
        const { data } = await axiosClient.put(`/projects/${id}`, { project }, { timeout: 2000 });
        return data;
    }

    async function updateMembersOfProject(projectid, memberids) {
        const { data } = await axiosClient.put(`/projects/${projectid}/users`, memberids, { timeout: 2000 });
        return data;
    }
    async function updateParentsOfProject(projectid, parentids) {
        const { data } = await axiosClient.put(`/projects/${projectid}/parents`, parentids, { timeout: 2000 });
        return data;
    }


    async function updateChildrenOfProject(projectid, childids) {
        const { data } = await axiosClient.put(`/projects/${projectid}/children`, childids, { timeout: 2000 });
        return data;
    }

    return {
        getProjects,
        getProjectById,
        deleteProject,
        archiveProject,
        getProjectsByUser,
        getParentsById,
        getChildrenById,
        addProject,
        updateProjectNameDescription,
        updateChildrenOfProject,
        updateMembersOfProject,
        updateParentsOfProject


    }



}
export default ProjectService();
