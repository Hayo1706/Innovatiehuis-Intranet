import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var ProjectService = function () {

    async function getProjects() {
        const response = await axiosClient.get('/projects', { timeout: 2000 });
        response.data.result.forEach(project => { 
            project.created = jsonToJsDate(project.created) 
            project.last_updated = jsonToJsDate(project.last_updated)
        });
        return response;
    }
    async function getProjectById(projectid) {
        const response = await axiosClient.get(`/projects/${projectid}`, { timeout: 2000 });
        response.data.result.forEach(project => { 
            project.created = jsonToJsDate(project.created) 
            project.last_updated = jsonToJsDate(project.last_updated)
        });
        return response;
    }
    async function deleteProject(id) {
        const response = await axiosClient.delete(`/projects/${id}`, { timeout: 2000 });
        return response;
    }
    async function archiveProject(project) {
        const response = await axiosClient.put(`/projects/${project.projectid}/archive`, { project }, { timeout: 2000 });
        return response;
    }
    async function getProjectsByUser(userid) {
        const response = await axiosClient.get(`/users/${userid}/projects`, { timeout: 2000 });
        response.data.result.forEach(project => { 
            project.created = jsonToJsDate(project.created) 
            project.last_updated = jsonToJsDate(project.last_updated)
            project.last_seen = jsonToJsDate(project.last_seen) 
        });
        return response;
    }
    async function getParentsById(projectid) {
        const response = await axiosClient.get(`/projects/${projectid}/parents`, { timeout: 2000 });
        response.data.result.forEach(project => { 
            project.created = jsonToJsDate(project.created) 
            project.last_updated = jsonToJsDate(project.last_updated)
        });
        return response;
    }
    async function getChildrenById(projectid) {
        const response = await axiosClient.get(`/projects/${projectid}/children`, { timeout: 2000 });
        response.data.result.forEach(project => { 
            project.created = jsonToJsDate(project.created) 
            project.last_updated = jsonToJsDate(project.last_updated)
        });
        return response;
    }
    async function addProject(project) {
        const response = await axiosClient.post(`/projects`, { project }, { timeout: 2000 });
        return response;
    }
    async function updateProjectNameDescription(id, project) {
        const response = await axiosClient.put(`/projects/${id}`, { project }, { timeout: 2000 });
        return response;
    }
    async function updateMembersOfProject(projectid, memberids) {
        const response = await axiosClient.put(`/projects/${projectid}/users`, memberids, { timeout: 2000 });
        return response;
    }
    async function updateParentsOfProject(projectid, parentids) {
        const response = await axiosClient.put(`/projects/${projectid}/parents`, parentids, { timeout: 2000 });
        return response;
    }
    async function updateChildrenOfProject(projectid, childids) {
        const response = await axiosClient.put(`/projects/${projectid}/children`, childids, { timeout: 2000 });
        return response;
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
