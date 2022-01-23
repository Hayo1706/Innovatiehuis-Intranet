import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var AnouncementService = function () {

    async function getAnnouncementsByProject(projectid) {
        if (typeof projectid == 'undefined') {
            const response = await axiosClient.get(`/announcements`, { timeout: 2000 });
            response.data.result.forEach(announcement => { announcement.timestamp = jsonToJsDate(announcement.timestamp) });
            return response;
        } else {
            const response = await axiosClient.get(`/projects/${projectid}/announcements`, { timeout: 2000 });
            response.data.result.forEach(announcement => { announcement.timestamp = jsonToJsDate(announcement.timestamp) });
            return response;
        }
    }
    async function postAnnouncement(projectid, announcement) {
        if (typeof projectid == 'undefined') {
            const response = await axiosClient.post(`/announcements`, { announcement }, { timeout: 2000 });
            return response;
        } else {   
            const response = await axiosClient.post(`/projects/${projectid}/announcements`, { announcement }, { timeout: 2000 });
            return response;
        }
    }
    async function deleteAnnouncement(announcementid) {
        const response = await axiosClient.delete(`/announcements/${announcementid}`, { timeout: 2000 });
        console.log("deleted announcement " + announcementid);
        return response;
    }
    async function editAnnouncement(announcementid, announcement) {
        const response = await axiosClient.put(`/announcements/${announcementid}`, { announcement }, { timeout: 2000 });
        return response;
    }
    async function getRepliesByAnnouncement(announcementid) {
        const response = await axiosClient.get(`/announcements/${announcementid}/replies`, { timeout: 2000 });
        response.data.result.forEach(reply => { reply.timestamp = jsonToJsDate(reply.timestamp) });
        return response;
    }
    async function addReply(announcementid, reply) {
        const response = await axiosClient.post(`/announcements/${announcementid}/replies`, { reply }, { timeout: 2000 });
        console.log("added Reply to announcement " + announcementid + ", reading: " + reply.content);
        return response;
    }
    async function deleteReply(replyid) {
        const response = await axiosClient.delete(`/replies/${replyid}`, { timeout: 2000 });
        console.log("deleted reply " + replyid);
        return response;
    }
    async function editReply(replyid, reply) {
        const response = await axiosClient.put(`/replies/${replyid}`, { reply }, { timeout: 2000 });
        return response;
    }

    return {
        getAnnouncementsByProject,
        postAnnouncement,
        deleteAnnouncement,
        editAnnouncement,
        getRepliesByAnnouncement,
        deleteReply,
        editReply,
        addReply
    }

}
export default AnouncementService();
