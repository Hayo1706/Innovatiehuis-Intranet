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

    async function deleteFolder(projectid, path, conf) {
        const { data } = await axiosClient.delete(`/projects/${projectid}/folders?path=` + path + `&conf=` + conf, { timeout: 2000 });
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

    async function uploadFiles(projectid, path, file, conf) {
        const { data } = await axiosClient.post(`/projects/${projectid}/files?path=` + path + `&conf=` + conf, file , { timeout: 20000 })
        return data
    }

    async function moveFile(projectid, from, to){
        const { data } = await axiosClient.put(`/projects/${projectid}/files`, {from, to} , { timeout: 20000 })
        return data
    }

    async function downloadFile(projectid, path) {
       const data = await axiosClient.get(`/projects/${projectid}/file?path=` + path, { responseType: "blob", timeout: 2000 })
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
        getFilesOfPath,
        uploadFiles,
        downloadFile,
        deleteFile,
        moveFile,
        renameFile,
        getFoldersOfProject,
        createFolder,
        deleteFolder,
        renameFolder,
        moveFolder
    }



}
export default FilestorageService();