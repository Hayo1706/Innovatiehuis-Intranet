import axios from 'axios';
//replace with correct url
const axiosClient = axios.create({
    baseURL: 'http://192.167.2.15:8080/'
});
export async function getProjects() {
    try {
        const { data } = await axiosClient.get('/projects', { timeout: 2000 });
        return [null, data]
    } catch (error) {
        if (!error.status) {
            // network error
            alert('Network error! Connection timed out!')
        }
        return [error]

    }
}
export async function deleteProject(id) {
    try {
        const { data } = await axiosClient.get(`/project/${id}`, { timeout: 2000 });
        return [null, data]
    } catch (error) {
        if (!error.status) {
            // network error
            alert('Network error! Connection timed out!')
        }
        return [error]

    }
}

export async function updateProject(project) {
    try {
        const { data } = await axiosClient.put(`/project/${project.id}`, { project }, { timeout: 2000 });
        return [null, data]
    } catch (error) {
        if (!error.status) {
            // network error
            alert('Network error! Connection timed out!')
        }
        return [error]

    }
}
