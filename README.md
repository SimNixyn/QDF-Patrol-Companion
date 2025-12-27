# QDF Patrol Companion

**Version**: `v0.4 alpha`  
**Author**: [simplynixyn](https://github.com/SimNixyn)

---

## 🛡️ Overview

QDF Patrol Companion is a Python-based companion tool for Roblox QDF operatives that provides:

- Real-time DMR temperature/status monitoring via F9 log scraping.
- Advanced integrity degradation simulations.
- Intelligent estimation logic when live data is delayed.

---

## ⚠️ Notices

> ❗ **Restricted Use**: This script includes antitamper mechanisms and will **only run if you are a member of the QDF Roblox group**. Unauthorized use triggers deterrent responses and exits execution.  
>
> ❗ **Data Disclaimer**: All data presented, including temperature readings, integrity estimations, and meltdown predictions, is derived from in-game logs and estimation algorithms. **This data is not guaranteed to be 100% accurate**. It is provided for general operational awareness only.

---

## 🧠 Features

- ✅ **Live Log Parsing** – Extracts DMR status and temp values from Roblox F9 logs.
- 🌡️ **Color-coded Temp Display** – Updates GUI with live temperature in Kelvin.
- 📉 **Reactor Integrity Simulation** – Simulates degradation based on thermal thresholds.
- 🧠 **Estimation Engine** – Predicts state when logs lag or data is missing.
- 🛡️ **Tamper Protection** – Script only executes if group membership is verified.

---

## 📦 Requirements

These packages are installed automatically on first run:

- `tkinter`
- `pygame`
- `pyaudio`
- `pydub`
- `numpy`
- `requests`
- `playsound`
- `win10toast`

> The script parses your `requirements.txt` and installs missing dependencies.
