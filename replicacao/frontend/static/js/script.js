const svg = d3.select("#chart").append("svg")
    .attr("width", "100%")
    .attr("height", "400px")  // Fixed height for SVG
    .attr("viewBox", "0 0 1200 400")
    .attr("preserveAspectRatio", "xMidYMid meet");

// Initialize the socket as a global variable
var socket = io("http://localhost:5000");

// Mapping status to pastel colors
const statusColors = {
    green: '#77dd77',
    blue: '#aec6cf',
    red: '#ff6961'
};

const tooltip = d3.select("#tooltip");

let selectedServer = null; // To store the currently selected server

function updateServers(servers) {
    const serverData = Object.keys(servers).map(key => ({
        name: key,
        status: servers[key].status,
        data: servers[key].data
    }));

    const circles = svg.selectAll("circle").data(serverData, d => d.name);

    circles.enter()
        .append("circle")
        .attr("class", "server")
        .attr("id", d => d.name)
        .attr("cx", (d, i) => 100 + i * 150)
        .attr("cy", 200)
        .attr("r", 40)
        .style("fill", d => statusColors[d.status])
        .on("click", function(event, d) {
            selectedServer = event['name']; // Update selected server
            fetchServerDetails(event['name']); // Fetch details for the clicked server
        })
        .merge(circles)
        .transition()
        .duration(500)
        .style("fill", d => statusColors[d.status]);

    circles.exit().remove();
}

socket.on("request_processed", updateServers);

// Initialize with server data
d3.json("http://localhost:5000/servers").then(updateServers);

function sendRequest() {
    const request = `data-${Math.floor(Math.random() * 100)}`;
    socket.emit('send_request', { request });
}

function sendFaultRequest() {
    const request = `data-${Math.floor(Math.random() * 100)}`;
    socket.emit('send_fault_request', { request });
}
