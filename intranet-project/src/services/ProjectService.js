import axios from 'axios';
import { jsonToJsDate } from './DataConverter';

var ProjectService = function () {
    const axiosClient = axios.create({
        baseURL: 'http://127.0.0.1:5000/api'
    });

    async function getProjects() {
        const { data } = await axiosClient.get('/projects', { timeout: 2000 });
        data.forEach(project => { project.createdat = jsonToJsDate(project.createdat) });
        data.forEach(project => { project.lastupdated = jsonToJsDate(project.lastupdated) });
        return data;
    }
    async function getProjectById(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}`, { timeout: 2000 });
        return data;
    }
    async function deleteProject(id) {
        const { data } = await axiosClient.delete(`/projects/${id}`, { timeout: 2000 });
        return data;
    }
    async function updateProject(project) {
        const { data } = await axiosClient.put(`/projects/${project.projectid}?isarchived=${project.isarchived}`, { timeout: 2000 });
        return data;
    }
    async function getProjectsByUser(userid) {
        const { data } = await axiosClient.get(`/users/${userid}/projects`, { timeout: 2000 });
        data.forEach(project => { project.lastupdated = jsonToJsDate(project.lastupdated) });
        return data;
    }






    async function getFoldersOfProject(projectid){
        const { data } = await axiosClient.get(`/projects/${projectid}/folders`, { timeout: 2000 });
        return data;
    }

    async function getFilesOfProject(projectid){
        const { data } = await axiosClient.get(`/projects/${projectid}/files`, { timeout: 2000 });
        return data;
    }
    
    async function createFolder(projectid, new_dir_name, current_path) {
        const { data } = await axiosClient.post(`/projects/${projectid}/folders`, { new_dir_name, current_path }, { timeout: 2000 });
        return data;
    }




    async function downloadFile(projectid, requested_path){
        const { data } = await axiosClient.get(`/projects/${projectid}/file`, { requested_path }, { timeout: 2000 })
        return data
    }
    async function uploadFile(projectid, current_path, file){
        const { data } = await axiosClient.post(`/projects/${projectid}/file`, { current_path, file }, { timeout: 2000 })
        return data
    }

    return {
        getProjects,
        getProjectById,
        deleteProject,
        updateProject,
        getProjectsByUser,
        uploadFile,
        downloadFile,
        getFoldersOfProject,
        getFilesOfProject, 
        createFolder       
    }



}
export default ProjectService();
