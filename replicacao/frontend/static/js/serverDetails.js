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

function fetchServerDetails(serverName) {
    console.log("Fetching details for:", serverName);
    fetch(`http://localhost:5000/servers`)
        .then(response => response.json())
        .then(servers => {
            const serverDetail = servers[serverName];
            if (serverDetail) {
                const statusDescription = getStatusDescription(serverDetail.status);
                detailsContent.innerHTML = `
                    <p><strong>Nome:</strong> ${serverName}</p>
                    <p><strong>Status:</strong> ${statusDescription}</p>
                    <p><strong>Dados Processados:</strong> ${serverDetail.data.join(", ")}</p>
                `;
                serverDetailsSection.classList.remove("hidden");
            } else {
                console.error('Server details not found for:', serverName);
            }
        })
        .catch(error => console.error('Error fetching server details:', error));
}

window.fetchServerDetails = fetchServerDetails;
