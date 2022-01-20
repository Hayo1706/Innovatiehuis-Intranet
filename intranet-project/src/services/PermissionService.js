var PermissionService = function () {

    function userHasPermission(permissionType) {
        if (localStorage.getItem("screening_status") != 1) {
            return false;
        }
        return localStorage.getItem(permissionType) == 1;
    }


    return {
        userHasPermission
    }



}
export default PermissionService();
