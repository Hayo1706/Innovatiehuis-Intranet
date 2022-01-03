import axiosClient from './AxiosClient';
//import { jsonToJsDate } from './DataConverter';

var FilestorageService = function () {


    async function getFoldersOfProject(projectid, path) {
        const { data } = await axiosClient.get(`/projects/${projectid}/folders?path=` + path, { timeout: 2000 });
        return data;
    }

    async function moveFolder(projectid, from, to, rename) {
        const { data } = await axiosClient.put(`/projects/${projectid}/folders`, { from, to, rename } , { timeout: 2000 });
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




    async function getFilesOfPath(projectid, path) {
        const { data } = await axiosClient.get(`/projects/${projectid}/files?path=` + path, { timeout: 2000 });
        return data;
    }

    async function uploadFiles(projectid, path, files) {
        const { data } = await axiosClient.post(`/projects/${projectid}/files?path=` + path, files , { timeout: 2000 })
        return data
    }

    async function downloadFile(projectid, path) {
       const data = await axiosClient.get(`/projects/${projectid}/file?path=` + path, { timeout: 2000 })
       return data
    }

    async function renameFile(projectid, path, name, type) {
        const { data } = await axiosClient.put(`/projects/${projectid}/file?path=` + path, { name, type }, { timeout: 2000 })
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
        getFilesOfPath,
        createFolder,
        deleteFolder,
        renameFolder,
        deleteFile,
        renameFile,
        moveFolder
    }



}
export default FilestorageService();