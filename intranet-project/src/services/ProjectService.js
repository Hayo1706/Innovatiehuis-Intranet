import axios from 'axios';

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

export async function getProjectsForUser(userid) {
    const { data } = await axiosClient.get(`/user/${userid}/projects`, { timeout: 2000 });
    return data;
}

export async function getAnnouncements(projectid) {
    const { data } = await axiosClient.get(`/project/${projectid}/announcements`, { timeout: 2000 });
    return data;
}
