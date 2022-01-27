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
            }, 1500);
        }, 5000);
    }

    function handleSuccess(response) {
        if (response.config.method == "get") {
            console.log("HTTP code " + response.status, "Successfully loaded resource:");
            console.log({response});
            return;
        }
        if (response.status) {
            console.log("HTTP code " + response.status, response.data.message);
            alert(response.data.message, "success");
            return;
        }
        console.log("HTTP code " + response.status, "Server returned the following response:");
        console.log({response});
    }

    function handleError(err) {
        if (err.code == "ECONNABORTED") {
            console.log({err});
            alert("De server reageert niet. Probeer het later opnieuw of neem contact op met de beheerder.", "error");
            return;
        }
        if (err.response.data.message) {
            console.log("HTTP code " + err.response.status, err.response.data.message);
            console.log({err});
            alert(err.response.status + " ERROR: " + err.response.data.message, "error");
            return;
        }
        if (err.response.status) {
            console.log("HTTP code " + err.response.status, err.response.statusText);
            console.log({err});
            alert(err.response.status + " ERROR: " + err.response.statusText, "error");
            return;
        }
        console.log("UNEXPECTED ERROR WHILE QUERYING DATA:");
        console.log({err});
        alert("Er is een onverwachte fout opgetreden. Neem contact op met de beheerder.", "error");
    }

    return {
        alert,
        handleSuccess,
        handleError
    }
}

export default AlertService();