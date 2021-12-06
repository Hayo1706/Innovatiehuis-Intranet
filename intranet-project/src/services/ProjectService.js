import axios from 'axios';
import { jsonToJsDate } from './DataConverter';




var ProjectService = function () {
    const axiosClient = axios.create({
        baseURL: 'http://127.0.0.1:5000/api'
    });

    async function getProjects() {
        const { data } = await axiosClient.get('/projects', { timeout: 2000 });
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
    async function getAnnouncementsByProject(projectid) {
        const { data } = await axiosClient.get(`/projects/${projectid}/announcements`, { timeout: 2000 });
        data.forEach(announcement => { announcement.timestamp = jsonToJsDate(announcement.timestamp) });
        return data;
    }
    async function postAnnouncement(projectid, announcement) {
        const { data } = await axiosClient.post(`/projects/${projectid}/announcements`, { announcement }, { timeout: 2000 });
        return data;
    }
    async function deleteAnnouncement(announcementid) {
        console.log("deleted announcement " + announcementid);
    }

    async function editAnnouncement(announcementid, content) {
        console.log("announcement " + announcementid + " now reads: " + content);
    }

    async function addComment(announcementid, content) {
        console.log("added comment to announcement " + announcementid + ", reading: " + content);
    }


    return {
        getProjects: getProjects,
        deleteProject: deleteProject,
        updateProject: updateProject,
        getProjectsByUser: getProjectsByUser,
        getAnnouncementsByProject: getAnnouncementsByProject,
        postAnnouncement: postAnnouncement,
        deleteAnnouncement: deleteAnnouncement,
        editAnnouncement: editAnnouncement,
        addComment: addComment
    }

}
export default ProjectService();
