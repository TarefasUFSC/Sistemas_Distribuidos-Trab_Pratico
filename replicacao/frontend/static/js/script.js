const svg = d3.select("#chart").append("svg")
    .attr("width", "100%")
    .attr("height", "400px")  // Definir uma altura fixa para o SVG
    .attr("viewBox", "0 0 1200 400")
    .attr("preserveAspectRatio", "xMidYMid meet");

const socket = io("http://localhost:5000");

// Mapear status para cores pastel
const statusColors = {
    green: '#77dd77',
    blue: '#aec6cf',
    red: '#ff6961'
};

const tooltip = d3.select("#tooltip");

function updateServers(servers) {
    console.log("Servers data received:", servers);  // Log the received data
    const serverData = Object.keys(servers).map(key => ({
        name: key,
        status: servers[key].status,
        data: servers[key].data
    }));

    console.log("Processed server data:", serverData);  // Log the processed server data

    const circles = svg.selectAll("circle").data(serverData, d => d.name);

    circles.enter()
        .append("circle")
        .attr("class", "server")
        .attr("id", d => d.name)  // Set the circle ID to the server name
        .attr("cx", (d, i) => 100 + i * 150)
        .attr("cy", 200)
        .attr("r", 40)
        .style("fill", d => statusColors[d.status])
        .on("click", function(event, d) {
            console.log("Circle clicked:");
            console.log("Event:", event);
            console.log("Data:", d);
            console.log("Server name:", event['name']);
            fetchServerDetails(event['name']);
        })
        .merge(circles)
        .transition()
        .duration(500)
        .style("fill", d => statusColors[d.status]);

    circles.exit().remove();
}

socket.on("request_processed", updateServers);

// Inicializar
d3.json("http://localhost:5000/servers").then(updateServers);

function sendRequest() {
    const request = `data-${Math.floor(Math.random() * 100)}`;
    socket.emit('send_request', { request });
}

function sendFaultRequest() {
    const request = `data-${Math.floor(Math.random() * 100)}`;
    socket.emit('send_fault_request', { request });
}
