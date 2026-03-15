from flask import Flask, render_template_string
import os
from collections import Counter

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "probe_logs.log")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BioEcho Shield SOC Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fb;
            margin: 0;
            padding: 20px;
            color: #222;
        }

        h1 {
            color: #1f3c88;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 20px;
        }

        .top-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }

        .card h3 {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #1f3c88;
        }

        .metric {
            font-size: 28px;
            font-weight: bold;
        }

        .threat-high { color: #dc3545; }
        .threat-medium { color: #fd7e14; }
        .threat-low { color: #28a745; }

        .status-active {
            display: inline-block;
            padding: 6px 12px;
            background: #d4edda;
            color: #155724;
            border-radius: 18px;
            font-weight: bold;
        }

        .section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            margin-bottom: 25px;
        }

        .section h2 {
            margin-top: 0;
            color: #1f3c88;
        }

        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }

        canvas {
            max-height: 320px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #ddd;
            font-size: 14px;
        }

        th {
            background-color: #eef3ff;
            color: #1f3c88;
        }

        tr:hover {
            background-color: #f9fbff;
        }

        .severity-high {
            color: white;
            background: #dc3545;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .severity-medium {
            color: white;
            background: #fd7e14;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .severity-low {
            color: white;
            background: #28a745;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .status-open {
            font-weight: bold;
            color: #dc3545;
        }

        .status-investigating {
            font-weight: bold;
            color: #fd7e14;
        }

        .status-resolved {
            font-weight: bold;
            color: #28a745;
        }

        .search-box {
            margin-top: 10px;
            margin-bottom: 15px;
        }

        .search-box input {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 14px;
        }

        .footer-note {
            color: #666;
            font-size: 13px;
            margin-top: 10px;
        }

        @media (max-width: 1200px) {
            .top-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            .charts-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 700px) {
            .top-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 500px) {
            .top-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <script>
        function filterTable(inputId, tableId) {
            let input = document.getElementById(inputId);
            let filter = input.value.toLowerCase();
            let table = document.getElementById(tableId);
            let tr = table.getElementsByTagName("tr");

            for (let i = 1; i < tr.length; i++) {
                let rowText = tr[i].textContent.toLowerCase();
                tr[i].style.display = rowText.includes(filter) ? "" : "none";
            }
        }
    </script>
</head>
<body>
    <h1>BioEcho Shield SOC Dashboard</h1>
    <div class="subtitle">Real-time monitoring of probe events, alerts, severity levels, and threat analytics</div>

    <div class="top-grid">
        <div class="card">
            <h3>Total Events</h3>
            <div class="metric">{{ total_logs }}</div>
        </div>

        <div class="card">
            <h3>Total Alerts</h3>
            <div class="metric">{{ total_alerts }}</div>
        </div>

        <div class="card">
            <h3>High Severity</h3>
            <div class="metric threat-high">{{ high_count }}</div>
        </div>

        <div class="card">
            <h3>Medium Severity</h3>
            <div class="metric threat-medium">{{ medium_count }}</div>
        </div>

        <div class="card">
            <h3>Low Severity</h3>
            <div class="metric threat-low">{{ low_count }}</div>
        </div>

        <div class="card">
            <h3>System Status</h3>
            <div class="status-active">ACTIVE</div>
        </div>

        <div class="card">
            <h3>Threat Level</h3>
            <div class="metric {% if threat_level == 'HIGH' %}threat-high{% elif threat_level == 'MEDIUM' %}threat-medium{% else %}threat-low{% endif %}">
                {{ threat_level }}
            </div>
        </div>

        <div class="card">
            <h3>Last Attack Time</h3>
            <div style="font-weight:bold;">{{ last_attack_time }}</div>
        </div>

        <div class="card">
            <h3>Last Refresh</h3>
            <div style="font-weight:bold;">Auto every 5 sec</div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="section">
            <h2>Attack Type Distribution</h2>
            <canvas id="attackTypeChart"></canvas>
        </div>

        <div class="section">
            <h2>Severity Distribution</h2>
            <canvas id="severityChart"></canvas>
        </div>
    </div>

    <div class="section">
        <h2>Probe Event Logs</h2>
        <div class="search-box">
            <input type="text" id="logSearch" onkeyup="filterTable('logSearch', 'logTable')" placeholder="Search probe events...">
        </div>
        <table id="logTable">
            <tr>
                <th>#</th>
                <th>Event Details</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ log }}</td>
            </tr>
            {% endfor %}
        </table>
        <div class="footer-note">Showing all captured probe activity from the log file.</div>
    </div>

    <div class="section">
        <h2>Detected Alerts</h2>
        <div class="search-box">
            <input type="text" id="alertSearch" onkeyup="filterTable('alertSearch', 'alertTable')" placeholder="Search alerts...">
        </div>
        <table id="alertTable">
            <tr>
                <th>#</th>
                <th>Severity</th>
                <th>Alert Type</th>
                <th>Status</th>
                <th>Time</th>
                <th>Alert Message</th>
            </tr>
            {% for alert in alerts %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>
                    {% if alert.severity == "HIGH" %}
                        <span class="severity-high">HIGH</span>
                    {% elif alert.severity == "MEDIUM" %}
                        <span class="severity-medium">MEDIUM</span>
                    {% else %}
                        <span class="severity-low">LOW</span>
                    {% endif %}
                </td>
                <td>{{ alert.type }}</td>
                <td>
                    {% if alert.status == "Open" %}
                        <span class="status-open">{{ alert.status }}</span>
                    {% elif alert.status == "Investigating" %}
                        <span class="status-investigating">{{ alert.status }}</span>
                    {% else %}
                        <span class="status-resolved">{{ alert.status }}</span>
                    {% endif %}
                </td>
                <td>{{ alert.time }}</td>
                <td>{{ alert.message }}</td>
            </tr>
            {% endfor %}
        </table>
        <div class="footer-note">Alerts are generated when suspicious probe interactions are found.</div>
    </div>

    <script>
        const attackTypeCtx = document.getElementById('attackTypeChart');
        new Chart(attackTypeCtx, {
            type: 'pie',
            data: {
                labels: {{ attack_labels | safe }},
                datasets: [{
                    data: {{ attack_values | safe }}
                }]
            },
            options: {
                responsive: true
            }
        });

        const severityCtx = document.getElementById('severityChart');
        new Chart(severityCtx, {
            type: 'bar',
            data: {
                labels: ['HIGH', 'MEDIUM', 'LOW'],
                datasets: [{
                    label: 'Severity Count',
                    data: [{{ high_count }}, {{ medium_count }}, {{ low_count }}]
                }]
            },
            options: {
                responsive: true
            }
        });
    </script>
</body>
</html>
"""

def classify_alert(log_line):
    text = log_line.lower()

    if "admin login" in text or "hidden admin panel" in text:
        return {
            "severity": "HIGH",
            "type": "Privilege Access Alert",
            "status": "Open"
        }
    elif "unauthorized file access" in text or "admin_credentials" in text:
        return {
            "severity": "HIGH",
            "type": "Sensitive File Access Alert",
            "status": "Open"
        }
    elif "multiple failed login attempts" in text:
        return {
            "severity": "MEDIUM",
            "type": "Brute Force Alert",
            "status": "Investigating"
        }
    else:
        return {
            "severity": "LOW",
            "type": "General Probe Alert",
            "status": "Resolved"
        }

def extract_attack_type(log_line):
    text = log_line.lower()

    if "admin login" in text:
        return "Fake Admin Login"
    elif "unauthorized file access" in text:
        return "Unauthorized File Access"
    elif "multiple failed login attempts" in text:
        return "Multiple Failed Logins"
    elif "hidden admin panel" in text:
        return "Hidden Admin Panel Probe"
    else:
        return "Other"

def extract_time_from_log(log_line):
    if "Time:" in log_line:
        return log_line.split("Time:")[-1].strip()
    return "N/A"

@app.route("/")
def home():
    logs = []
    alerts = []
    attack_counter = Counter()

    high_count = 0
    medium_count = 0
    low_count = 0
    last_attack_time = "N/A"

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            logs = [line.strip() for line in file.readlines() if line.strip()]

        for line in logs:
            if "PROBE_EVENT" in line:
                alert_info = classify_alert(line)
                attack_type = extract_attack_type(line)
                event_time = extract_time_from_log(line)

                attack_counter[attack_type] += 1

                if alert_info["severity"] == "HIGH":
                    high_count += 1
                elif alert_info["severity"] == "MEDIUM":
                    medium_count += 1
                else:
                    low_count += 1

                if event_time != "N/A":
                    last_attack_time = event_time

                alerts.append({
                    "message": f"Potential intrusion detected: {line}",
                    "severity": alert_info["severity"],
                    "type": alert_info["type"],
                    "status": alert_info["status"],
                    "time": event_time
                })

    if high_count > 0:
        threat_level = "HIGH"
    elif medium_count > 0:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    return render_template_string(
        HTML_PAGE,
        logs=logs,
        alerts=alerts,
        total_logs=len(logs),
        total_alerts=len(alerts),
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        threat_level=threat_level,
        last_attack_time=last_attack_time,
        attack_labels=list(attack_counter.keys()),
        attack_values=list(attack_counter.values())
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)