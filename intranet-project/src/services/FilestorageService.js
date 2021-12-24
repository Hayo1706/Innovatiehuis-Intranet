import axiosClient from './AxiosClient';
//import { jsonToJsDate } from './DataConverter';

var FilestorageService = function () {


    async function getFoldersOfProject(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/folders`, { timeout: 2000 });
        return data;
    }

    async function createFolder(projectid, path, name) {
        const { data } = await axiosClient.post(`/projects/${projectid}/folders?path=` + path, { name }, { timeout: 2000 });
        return data;
    }

    async function deleteFolder(projectid, path) {
        const { data } = await axiosClient.delete(`/projects/${projectid}/folders?path=` + path, { timeout: 2000 });
        return data;
    }

    async function renameFolder(projectid, from, to, rename) {
        const { data } = await axiosClient.put(`/projects/${projectid}/folders`, { from, to, rename }, { timeout: 2000 });
        return data;
    }




    async function getFilesOfProject(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/files`, { timeout: 2000 });
        return data;
    }

    async function uploadFiles(projectid, path, files) {
        const { data } = await axiosClient.post(`/projects/${projectid}/files?path=` + path, files , { timeout: 2000 })
        return data
    }

    async function downloadFile(projectid, path) {
        const { data } = await axiosClient.get(`/projects/${projectid}/file?path=` + path, { timeout: 2000 })
        return data
    }

    async function deleteFile(projectid, path) {
        const { data } = await axiosClient.delete(`/projects/${projectid}/file?path=` + path, { timeout: 2000 })
        return data
    }
    

    return {
        uploadFiles,
        downloadFile,
        getFoldersOfProject,
        getFilesOfProject,
        createFolder,
        deleteFolder,
        renameFolder,
        deleteFile,
    }



}
export default FilestorageService();