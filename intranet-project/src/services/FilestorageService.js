import axiosClient from './AxiosClient';
//import { jsonToJsDate } from './DataConverter';

var FilestorageService = function () {


    async function getFoldersOfProject(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/folders`, { timeout: 2000 });
        return data;
    }

    async function getFilesOfProject(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/files`, { timeout: 2000 });
        return data;
    }

    async function createFolder(projectid, new_dir_name, current_path) {
        const { data } = await axiosClient.delete(`/projects/${projectid}/folders`, { new_dir_name, current_path }, { timeout: 2000 });
        return data;
    }

    async function deleteFolder(projectid, dir_name, current_path, confirmation) {
        const { data } = await axiosClient.post(`/folders/${projectid}`, { dir_name, current_path, confirmation }, { timeout: 2000 });
        return data;
    }




    async function downloadFile(projectid, requested_path) {
        const { data } = await axiosClient.get(`/projects/${projectid}/file`, { requested_path }, { timeout: 2000 })
        return data
    }
    async function uploadFile(projectid, current_path, file) {
        const { data } = await axiosClient.post(`/projects/${projectid}/file`, { current_path, file }, { timeout: 2000 })
        return data
    }

    return {
        uploadFile,
        downloadFile,
        getFoldersOfProject,
        getFilesOfProject,
        createFolder,
        deleteFolder,
    }



}
export default FilestorageService();