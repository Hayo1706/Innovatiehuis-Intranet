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

    return {
        alert
    }
}

export default AlertService();