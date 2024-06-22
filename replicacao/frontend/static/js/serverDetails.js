const serverDetailsSection = document.getElementById("server-details");
const detailsContent = document.getElementById("details-content");

function getStatusDescription(status) {
    switch (status) {
        case 'blue':
            return 'Servidor backup em execução, pronto para assumir';
        case 'green':
            return 'Servidor principal em execução, tudo OK';
        case 'red':
            return 'Servidor principal inativo, backup assumiu';
        default:
            return 'Desconhecido'; // Handle any unexpected statuses
    }
}

socket.on("server_details_updated", serverDetail => {
    updateServerDetails(serverDetail);
});

function updateServerDetails(serverDetail) {
    if (selectedServer && serverDetail.name === selectedServer) { // Only update if the details are for the selected server
        const statusDescription = getStatusDescription(serverDetail.status);
        const processedDataList = serverDetail.processed_data.join(", ");
        const synchronizedDataList = serverDetail.synchronized_data.join(", ");

        detailsContent.innerHTML = `
            <p><strong>Nome:</strong> ${serverDetail.name}</p>
            <p><strong>Status:</strong> ${statusDescription}</p>
            <p><strong>Dados Processados:</strong> ${processedDataList}</p>
            <p><strong>Dados Sincronizados:</strong> ${synchronizedDataList}</p>
        `;
        serverDetailsSection.classList.remove("hidden");
    }
}

function fetchServerDetails(serverName) {
    socket.emit("fetch_server_details", serverName);
    selectedServer = serverName; // Update the selected server
}

// Expose fetchServerDetails globally
window.fetchServerDetails = fetchServerDetails;
