const svg = d3.select("#chart").append("svg")
    .attr("width", "100%")
    .attr("height", "400px")
    .attr("preserveAspectRatio", "xMidYMid meet");

var socket = io("http://localhost:5000");

// Mapping status to pastel colors
const statusColors = {
    green: '#77dd77',
    blue: '#aec6cf',
    red: '#ff6961'
};

const tooltip = d3.select("#tooltip");

let selectedServer = null; // To store the currently selected server
let requestCounter = localStorage.getItem('requestCounter') ? parseInt(localStorage.getItem('requestCounter')) : 1;

function updateServers(servers) {
    const serverData = Object.keys(servers).map(key => ({
        name: key,
        status: servers[key].status,
        data: servers[key].data
    }));

    const circles = svg.selectAll("circle").data(serverData, d => d.name);

    const numServersPerRow = 8;
    const circleSpacing = 150;
    const rowHeight = 100;
    const circleRadius = 40;

    // Calculate the number of rows needed
    const numRows = Math.ceil(serverData.length / numServersPerRow);

    // Update SVG viewBox and height dynamically
    const svgHeight = 100 + numRows * rowHeight;
    svg.attr("height", svgHeight)
       .attr("viewBox", `0 0 1200 ${svgHeight}`);

    circles.enter()
        .append("circle")
        .attr("class", "server")
        .attr("id", d => d.name)
        .attr("cx", (d, i) => 100 + (i % numServersPerRow) * circleSpacing)
        .attr("cy", (d, i) => 100 + Math.floor(i / numServersPerRow) * rowHeight)
        .attr("r", circleRadius)
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
    const request = `data-${requestCounter++}`;
    socket.emit('send_request', { request });
    localStorage.setItem('requestCounter', requestCounter); // Update local storage
}

function sendFaultRequest() {
    const request = `data-${requestCounter++}`;
    socket.emit('send_fault_request', { request });
    localStorage.setItem('requestCounter', requestCounter); // Update local storage
}
