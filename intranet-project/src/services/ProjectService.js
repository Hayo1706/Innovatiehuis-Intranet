import axios from 'axios';
import { sqlToJsDate } from './DataConverter';

const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api'
});

export async function getProjects() {
    const { data } = await axiosClient.get('/projects', { timeout: 2000 });
    return data;
}
export async function deleteProject(id) {
    const { data } = await axiosClient.delete(`/projects/${id}`, { timeout: 2000 });
    return data;
}

export async function updateProject(project) {
    const { data } = await axiosClient.put(`/projects/${project.projectid}?isarchived=${project.isarchived}`, { timeout: 2000 });
    return data;
}

export async function getProjectsByUser(userid) {
    const { data } = await axiosClient.get(`/users/${userid}/projects`, { timeout: 2000 });
    data.forEach(project => { project.lastupdated = sqlToJsDate(project.lastupdated) });
    return data;
}

export async function getAnnouncementsByProject(projectid) {
    const { data } = await axiosClient.get(`/projects/${projectid}/announcements`, { timeout: 2000 });
    data.forEach(announcement => { announcement.timestamp = sqlToJsDate(announcement.timestamp) });
    return data;
}

export async function postAnnouncement(projectid, announcement) {
    const { data } = await axiosClient.post(`/projects/${projectid}/announcements`, { announcement }, { timeout: 2000 });
    return data;
}

export async function deleteAnnouncement(announcementid) {
    console.log("deleted announcement " + announcementid);
}

export async function editAnnouncement(announcementid, content) {
    console.log("announcement " + announcementid + " now reads: " + content);
}

export async function addComment(announcementid, content) {
    console.log("added comment to announcement " + announcementid + ", reading: " + content);
}
