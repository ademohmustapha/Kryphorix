# 🛡️ Kryphorix — Advanced Security Assessment Framework

Kryphorix is a modular, professional security assessment and vulnerability scanning tool. It covers infrastructure, web applications, APIs, and Active Directory, designed for cybersecurity professionals and beginners alike.

---

## 🚀 Core Features

- Multi-surface security assessment
- Modular architecture (Web, API, Active Directory, Ports, TLS/SSL)
- Automatic PDF & JSON report generation
- Live scan dashboard with severity tracking
- Beginner-friendly CLI and menu interface
- Plugin support for extensibility

---

## 🏗️ Project Structure

```

Kryphorix/
│
├── main.py
├── requirements.txt
├── kryphorix.sh
│
├── modules/
│   ├── web.py
│   ├── api.py
│   ├── ad.py
│   ├── ports.py
│   └── tls.py
│
└── core/
├── findings.py
├── reporter.py
├── engine.py

````

---

## 🖥️ Installation Guide (Beginner-Friendly)

1. Clone the repository:

```bash
git clone https://github.com/ademohmustapha/Kryphorix.git
cd Kryphorix
````

2. Create a Python virtual environment (recommended):

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

* Linux/macOS:

```bash
source venv/bin/activate
```

* Windows (PowerShell):

```bash
venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

> ⚠️ Note: If you encounter an “externally-managed environment” error, ensure you are using a virtual environment (`venv`) as shown above.

---

## ▶️ Running Kryphorix

### Option 1: Beginner Menu Mode

```bash
python3 main.py
```

* Follow the on-screen menu.
* Choose a module (Web, API, AD, Ports, TLS).
* View real-time scan progress and summary.
* Reports (PDF + JSON) are automatically saved in the `reports/` folder.

### Option 2: Professional CLI Mode

```bash
python3 main.py --web https://example.com --api https://api.example.com --ad 192.168.1.10 --ports 192.168.1.10 --tls example.com
```

* Run multiple scans simultaneously.
* Generate combined reports automatically.
* Use `--fullscan <target>` to scan all modules at once.

---

## 📊 Reports

* PDF and JSON formats saved in the `reports/` folder.
* PDF includes:

  * Cover page with logo
  * Executive summary
  * Module & severity breakdown
  * Detailed findings table (color-coded by severity)
* JSON provides structured data for further analysis.

---

## ⚠️ Legal Disclaimer

Kryphorix is strictly for authorized security testing and educational purposes**.
The author is not responsible for misuse or unauthorized deployment.

---

## 👤 Author

Ademoh Mustapha Onimisi

Cybersecurity Egineering, Research & Tool Development

---

## 📜 License

Copyright © 2026 Ademoh Mustapha Onimisi
All rights reserved.
Unauthorized copying, distribution, or use of this tool without permission is prohibited.

---

## ⭐ Why Kryphorix?

Kryphorix is a professional-grade security framework, designed for extensibility, clear reporting, and beginner-to-pro user flexibility.

````

---

