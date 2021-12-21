import axiosClient from './AxiosClient';
import { jsonToJsDate } from './DataConverter';

var AnouncementService = function () {



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
    async function addReply(announcementid, reply) {
        const { data } = await axiosClient.post(`/announcements/${announcementid}/replies`, { reply }, { timeout: 2000 });
        console.log("added Reply to announcement " + announcementid + ", reading: " + reply.content);
        return data;
    }
    async function deleteReply(replyid) {
        const { data } = await axiosClient.delete(`/replies/${replyid}`, { timeout: 2000 });
        console.log("deleted reply " + replyid);
        return data;
    }
    async function editReply(replyid, reply) {
        const { data } = await axiosClient.put(`/replies/${replyid}`, { reply }, { timeout: 2000 });
        return data;
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
