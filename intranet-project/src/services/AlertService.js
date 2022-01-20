var AlertService = function () {
    function alert(message, type) {
        const alertEl = document.createElement("div");
        alertEl.innerHTML = `
        <div class="alert-bar ${type}">
            ${message}
        </div>
        `;
        alertEl.classList.add(type);
        document.querySelector("#alert-wrapper").appendChild(alertEl);

        setTimeout(function() {
            var seconds = 1;
            alertEl.style.transition = "opacity "+seconds+"s ease";
    
            alertEl.style.opacity = 0;
            setTimeout(function() {
                alertEl.remove();
            }, 1000);
        }, 4000);
    }

    function handleSuccess(response) {
        console.log(response.status, response.response.message);
        AlertService.alert(response.response.message, "success");
    }

    function handleError(err) {
        if (err.response) {
            alert(err.response.data.response.message, "error");
            console.log("HTTP code " + err.response.status);
            if (err.response.data.response.message) console.log(err.response.data.response.message);
          } else if (err.code == "ECONNABORTED") {
            alert("De server reageert niet. Probeer het later opnieuw of neem contact op met de beheerder.", "error");
            console.log({err});
          } else {
            alert("Er is een onverwachte fout opgetreden. Neem contact op met de beheerder.", "error");
            console.log({err});
          }
    }

    return {
        alert,
        handleSuccess,
        handleError
    }
}

export default AlertService();