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
    const { data } = await axiosClient.delete(`/project/${id}`, { timeout: 2000 });
    return data;
}

export async function updateProject(project) {
    const { data } = await axiosClient.put(`/project/${project.projectid}`, { project }, { timeout: 2000 });
    return data;
}

export async function getProjectsByUser(userid) {
    const { data } = await axiosClient.get(`/user/${userid}/projects`, { timeout: 2000 });
    data.forEach(project => { project.lastupdated = sqlToJsDate(project.lastupdated)});
    return data;
}

export async function getAnnouncementsByProject(projectid) {
    const { data } = await axiosClient.get(`/project/${projectid}/announcements`, { timeout: 2000 });
    data.forEach(announcement => { announcement.timestamp = sqlToJsDate(announcement.timestamp)});
    return data;
}

export async function postAnnouncement(projectid, announcement) {
    const { data } = await axiosClient.post(`/project/${projectid}/announcements`, { announcement }, { timeout: 2000 });
    return data;
}
