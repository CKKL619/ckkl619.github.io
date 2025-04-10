const validUser = {
    username: "Security",
    password: "EVchargeSecurity"
};

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username === validUser.username && password === validUser.password) {
        document.getElementById('login-page').style.display = 'none';
        document.getElementById('main-content').style.display = 'flex';
        showPage('home');
    } else {
        alert('Invalid credentials');
    }
}

function showPage(pageId) {
    // Remove active class from all buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    document.querySelector(`[onclick="showPage('${pageId}')"]`).classList.add('active');
    
    // Show the selected page
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.style.display = 'none');
    document.getElementById(pageId).style.display = 'block';
}

// Charger Page Functions
let records = []; // This would be populated with actual data from the server

function toggleCharger() {
    const chargerSwitch = document.getElementById('charger-switch');
    const status = chargerSwitch.checked ? 'ON' : 'OFF';
    // Send status to server
    console.log(`Charger status set to: ${status}`);
}

function searchCharger() {
    const chargerId = document.getElementById('charger-search').value;
    // Fetch charger data from server
    console.log(`Searching for charger: ${chargerId}`);
}

function generateLog() {
    // Generate log from records
    const log = records.map(record => 
        `ID: ${record.chargerid}, Status: ${record.chargingStatus}, Time: ${record.chargingTime}`
    ).join('\n');
    console.log('Generated Log:\n', log);
}

function exportExcel() {
    // Convert records to Excel
    const worksheet = XLSX.utils.json_to_sheet(records);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Charger Data");
    XLSX.writeFile(workbook, "charger_data.xlsx");
}

// Chart Initialization
function initChargerChart() {
    const ctx = document.getElementById('charger-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: records.map(record => record.chargingTime),
            datasets: [{
                label: 'Charging Status',
                data: records.map(record => record.chargingStatus === 'Charging' ? 1 : 0),
                borderColor: '#1e3c72',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value === 1 ? 'Charging' : 'Idle';
                        }
                    }
                }
            }
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('charger-chart')) {
        initChargerChart();
    }
});

// Temperature & Humidity Sensor Functions
let sensorRecords = []; // This would be populated with actual data from the server

function toggleSensor() {
    const sensorSwitch = document.getElementById('sensor-switch');
    const status = sensorSwitch.checked ? 'ON' : 'OFF';
    // Send status to server
    console.log(`Sensor status set to: ${status}`);
}

function searchSensor() {
    const sensorId = document.getElementById('sensor-search').value;
    // Fetch sensor data from server
    console.log(`Searching for sensor: ${sensorId}`);
}

function generateSensorLog() {
    // Generate log from sensor records
    const log = sensorRecords.map(record => 
        `Time: ${record.time}, Power: ${record.power}, Temp: ${record.temperature}°C, Humidity: ${record.humidity}%`
    ).join('\n');
    console.log('Generated Sensor Log:\n', log);
}

function exportSensorExcel() {
    // Convert sensor records to Excel
    const worksheet = XLSX.utils.json_to_sheet(sensorRecords);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Sensor Data");
    XLSX.writeFile(workbook, "sensor_data.xlsx");
}

// Chart Initialization for Temperature & Humidity
function initTempHumidityChart() {
    const ctx = document.getElementById('temp-humidity-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sensorRecords.map(record => record.time),
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: sensorRecords.map(record => record.temperature),
                    borderColor: '#ff6384',
                    fill: false
                },
                {
                    label: 'Humidity (%)',
                    data: sensorRecords.map(record => record.humidity),
                    borderColor: '#36a2eb',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('temp-humidity-chart')) {
        initTempHumidityChart();
    }
});

// Human Motion Sensor Functions
let motionRecords = []; // This would be populated with actual data from the server

function toggleMotionSensor() {
    const motionSwitch = document.getElementById('motion-switch');
    const status = motionSwitch.checked ? 'ON' : 'OFF';
    // Send status to server
    console.log(`Motion sensor status set to: ${status}`);
}

function searchMotionSensor() {
    const sensorId = document.getElementById('motion-search').value;
    // Fetch sensor data from server
    console.log(`Searching for motion sensor: ${sensorId}`);
}

function generateMotionLog() {
    // Generate log from motion records
    const log = motionRecords.map(record => 
        `Time: ${record.time}, Power: ${record.power}, Activity: ${record.ispresence ? 'Detected' : 'No Activity'}`
    ).join('\n');
    console.log('Generated Motion Log:\n', log);
}

function exportMotionExcel() {
    // Convert motion records to Excel
    const worksheet = XLSX.utils.json_to_sheet(motionRecords);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Motion Data");
    XLSX.writeFile(workbook, "motion_data.xlsx");
}

// Chart Initialization for Motion Sensor
function initMotionChart() {
    const ctx = document.getElementById('motion-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: motionRecords.map(record => record.time),
            datasets: [
                {
                    label: 'Human Activity',
                    data: motionRecords.map(record => record.ispresence ? 1 : 0),
                    borderColor: '#4caf50',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value === 1 ? 'Activity' : 'No Activity';
                        }
                    }
                }
            }
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('motion-chart')) {
        initMotionChart();
    }
});

// Water Leak Sensor Functions
let waterRecords = []; // This would be populated with actual data from the server

function toggleWaterSensor() {
    const waterSwitch = document.getElementById('water-switch');
    const status = waterSwitch.checked ? 'ON' : 'OFF';
    // Send status to server
    console.log(`Water sensor status set to: ${status}`);
}

function searchWaterSensor() {
    const sensorId = document.getElementById('water-search').value;
    // Fetch sensor data from server
    console.log(`Searching for water sensor: ${sensorId}`);
}

function generateWaterLog() {
    // Generate log from water records
    const log = waterRecords.map(wlrecords => 
        `Time: ${wlrecords.time}, Power: ${wlrecords.power}, Leak: ${wlrecords.isleak ? 'unknown' : 'No Leak'}`
    ).join('\n');
    console.log('Generated Water Log:\n', log);
}

function exportWaterExcel() {
    // Convert water records to Excel
    const worksheet = XLSX.utils.json_to_sheet(waterRecords);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Water Data");
    XLSX.writeFile(workbook, "water_data.xlsx");
}

// Chart Initialization for Water Sensor
function initWaterChart() {
    const ctx = document.getElementById('water-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: waterRecords.map(record => record.time),
            datasets: [
                {
                    label: 'Water Leak',
                    data: waterRecords.map(record => record.isleak ? 1 : 0),
                    borderColor: '#2196f3',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value === 1 ? 'Leak' : 'No Leak';
                        }
                    }
                }
            }
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('water-chart')) {
        initWaterChart();
    }
}); 

document.getElementById("toggleSwitch").addEventListener("change", function() {
    if (this.checked) {
        fetch("/toggleChargerTrue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "true" }) }
        ).then(response => {
            if (response.ok) {
                console.log("Toggle switched to true"); }
            else {
                console.error("Failed to send request"); } }).catch(error => {console.error("Error:", error); }); }
    else {
        fetch("/toggleChargerFalse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "false" }) }
        ).then(response => {
            if (response.ok) {
                console.log("Toggle switched to false"); }
            else {
                console.error("Failed to send request"); } }).catch(error => { console.error("Error:", error); }); } });