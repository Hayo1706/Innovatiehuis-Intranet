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
        if (typeof projectid == 'undefined') {
            const { data } = await axiosClient.get(`/announcements`, { timeout: 2000 });
            data.forEach(announcement => { announcement.timestamp = jsonToJsDate(announcement.timestamp) });
            return data;
        } else {
            const { data } = await axiosClient.get(`/projects/${projectid}/announcements`, { timeout: 2000 });
            data.forEach(announcement => { announcement.timestamp = jsonToJsDate(announcement.timestamp) });
            return data;
        }
    }
    async function postAnnouncement(projectid, announcement) {
        if (typeof projectid == 'undefined') {
            const { data } = await axiosClient.post(`/announcements`, { announcement }, { timeout: 2000 });
            return data;
        } else {
            const { data } = await axiosClient.post(`/projects/${projectid}/announcements`, { announcement }, { timeout: 2000 });
            return data;
        }
    }
    async function deleteAnnouncement(announcementid) {
        const { data } = await axiosClient.delete(`/announcements/${announcementid}`, { timeout: 2000 });
        console.log("deleted announcement " + announcementid);
        return data;
    }

    async function editAnnouncement(announcementid, announcement) {
        const { data } = await axiosClient.put(`/announcements/${announcementid}`, { announcement }, { timeout: 2000 });
        return data;
    }

    async function getRepliesByAnnouncement(announcementid) {
        const { data } = await axiosClient.get(`/announcements/${announcementid}/replies`, { timeout: 2000 });
        data.forEach(reply => { reply.timestamp = jsonToJsDate(reply.timestamp) });
        return data;
    }

    async function addReply(announcementid, Reply) {
        const { data } = await axiosClient.post(`/announcements/${announcementid}/Replys`, { Reply }, { timeout: 2000 });
        console.log("added Reply to announcement " + announcementid + ", reading: " + Reply.content);
        return data;
    }


    return {
        getProjects,
        deleteProject,
        updateProject,
        getProjectsByUser,
        getAnnouncementsByProject,
        postAnnouncement,
        deleteAnnouncement,
        editAnnouncement,
        getRepliesByAnnouncement,
        addReply
    }

}
export default ProjectService();
