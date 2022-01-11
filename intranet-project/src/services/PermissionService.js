var PermissionService = function () {

    function userHasPermission(permissionType) {
        if (localStorage.getItem("screening_status") != 2) {
            return false;
        }
        return localStorage.getItem(permissionType) == 1;
    }


    return {
        userHasPermission
    }



}
export default PermissionService();
