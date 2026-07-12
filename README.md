# Acme Secret Santa Automator

A modular, extensible, and cloud-ready Object-Oriented Secret Santa system that automates employee gift assignments while strictly avoiding repetitive gift pairings from the previous year.

## 🛠️ Project Structure Overview
- models/: Encapsulates core data schemas (Employee and SecretSantaAssignment).
- services/csv_handler.py: Dedicated I/O engine parsing incoming datasets and formatting exports.
- services/matcher.py: Core rule matching logic verifying constraints.
- templates/index.html: Responsive frontend web-dashboard interface.
- main.py: Main orchestration wrapper and API engine entrypoint.

## 🚀 Execution Instructions

### Option 1: Standalone Application (No Setup Needed)
1. Navigate to the dist/ directory.
2. Double-click main.exe. Your default web browser will automatically open to the user interface panel.

### Option 2: Run via Local Development Environment
1. Ensure dependencies are satisfied:
   bash
   pip install -r requirements.txt
   
2. Fire up the local server pipeline:
   bash
   python main.py
   
3. Open your browser and navigate to: http://127.0.0.1:8000