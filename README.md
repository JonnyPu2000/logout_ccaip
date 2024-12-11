# User  Manager for CCAIP

This project is designed for managing user statuses in teams using the Contact Center AI Platform (CCAIP). It allows you to collect the names and IDs of users, monitor their statuses, and enforce logout actions based on specific criteria (status other than "Available" and inactivity for more than 3 hours). The project features a graphical user interface (GUI) built with Tkinter, enabling interaction with the data and presenting it in an organized table format.

---

## 🚀 Features

- **Collect Team Names and IDs**: Gather agent names and IDs from selected teams.
- **Status Monitoring and Inactivity Tracking**: Display the current status of agents and the time they’ve spent in the same status.
- **Force Logout**: Logout agents who are not in "Available" status and have stayed in the same status for more than 3 hours.
- **Graphical User Interface**: A simple interface to select teams, view statuses, and force logouts.
- **Notifications**: Display pop-up messages to inform the user about the success or failure of logout attempts.

---

## 📋 Requirements

Ensure that you have the following installed:

- **Python 3.x**
- Libraries:
  - `tkinter` (for the graphical user interface)
  - `requests` (to make HTTP requests)
  - `datetime` (for date and time manipulation)

---

## ⚙️ Installation

1. Clone the repository or download the project files:
   `git clone https://github.com/JonnyPu2000/logout_ccaip`

2. Install the required dependencies:
  ` pip install requirements.txt`

3. Configure the API URL and token in the config/config.py file to match your CCAIP instance.

## 🖥️ How to Use

### Collect Team IDs and Names:

1. Open the GUI.
2. Select the teams from which you want to collect information.
3. Click on the **"Collect IDs and Names"** button to display tables with the agents' status information.

### Force Logout:

1. After collecting the data, select the teams for which you want to force agent logouts.
2. Click on the **"Force Logout"** button to apply the logout rules.

### Notification Popups:

- A popup will appear after attempting to logout an agent, indicating whether the action was successful or the reason for failure.

---

## 🏗️ Architecture

The code is organized into the following modules:

- **`interface.py`**: Contains all the logic for the graphical user interface (using Tkinter), collecting data, and displaying tables.
- **`getTeams.py`**: Contains functions to fetch team and assignee information.
- **`postLogout.py`**: Contains functions to send requests to force logout agents.
- **`config.py`**: Configuration file where you define the API URL and authentication token.
- **`README.md`**: This document, explaining the project setup and usage.

---

## 🛠️ Example Configuration (`config/config.py`)

```python
BASE_URL = 'https://api.example.com'  # Base URL of the CCAIP API
TOKEN = 'your_token_here'  # Your CCAIP API authentication token
TEAM_IDS = [123, 456, 789]  # IDs of the teams to manage
```

---
## 🤝 Contribution
If you'd like to contribute to this project, feel free to open a pull request or submit an issue to discuss improvements and fixes.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software in accordance with the license terms.



