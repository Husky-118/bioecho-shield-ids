BioEcho Shield IDS – Probe-Based Intrusion Detection System

Overview
BioEcho Shield IDS is a probe-based Intrusion Detection System (IDS) designed to detect unauthorized activities within a system.
Instead of waiting for real system components to be attacked, the system deploys decoy probe files that act as monitoring triggers.
Whenever an attacker or unauthorized user interacts with these probe files, the system logs the event, analyzes the activity, generates alerts,
and visualizes the incident through a SOC-style monitoring dashboard.
This approach helps security analysts quickly identify suspicious behavior and monitor potential intrusion attempts in real time

Objective
The primary objective of this project is to design and implement a probe-based intrusion detection 
framework that can detect suspicious or unauthorized activities within a system environment.
The system works by placing strategically designed probe files within the system.
These probe files act as security sensors. When an attacker attempts to access these files,
the system captures the event details and generates alerts for monitoring and analysis.
The project also includes a Security Operations Center (SOC) dashboard that visually represents detected probe events, 
severity levels, and attack statistics to help security analysts monitor potential threats effectively.

Key Features
-->Probe-Based Intrusion Detection
The system uses specially designed probe files that act as triggers to detect unauthorized access attempts.
-->Unauthorized Access Monitoring
Whenever a probe file is accessed, the system immediately logs the event and records details such as timestamp, event ID, and access type.
-->Event Logging System
All probe events are stored in structured logs, enabling further security analysis and investigation.
-->Alert Generation Mechanism
When suspicious activity is detected, the system automatically generates alerts to indicate possible security threats.
-->SOC Monitoring Dashboard
A real-time SOC-style dashboard visualizes:
	•	Total security events
	•	Generated alerts
	•	Threat severity levels
	•	Attack statistics
-->Threat Classification
Detected activities are categorized into different severity levels such as:
	•	High
	•	Medium
	•	Low
-->Attack Trend Visualization
The dashboard displays charts showing patterns and frequency of probe access attempts.

Technologies Used
-->Programming Language:
Python
-->Backend Framework:
Flask
-->Visualization:
HTML + Flask templating
-->Logging and Detection:
Custom Python-based detection engine
-->Version Control:
Git

How the System Works
	1.	Probe files are deployed within the system environment.
	2.	These probe files act as security sensors designed to detect unauthorized access attempts.
	3.	When an attacker or unauthorized user interacts with a probe file, the system detects the activity.
	4.	The detection engine records the event details and stores them in system logs.
	5.	The alert system evaluates the event and generates a security alert if suspicious behavior is identified.
  6.	The SOC dashboard displays the detected events, alerts, and threat levels in a visual format.
 
Running the Project
-->Install dependencies:
CODE
pip install -r requirements.txt
-->Run the IDS system:
python main.py
-->Open the dashboard in your browser:
http://127.0.0.1:/5000

Example Detection Event
When a probe file is accessed the system logs a event simular to
CODE
PROBE_EVENT | ID:20260315144509 | Unauthorized file access attempt on  Admin_Credentials.txt

Applications

This probe-based IDS system can be used for:
	•	Security monitoring
	•	Insider threat detection
	•	Unauthorized access detection
	•	Cybersecurity research
	•	Educational demonstrations of intrusion detection systems

Repository Hosting

GitHub
