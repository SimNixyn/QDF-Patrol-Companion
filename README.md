# QDF Patrol Companion

**Version**: `v0.5 alpha`  
**Author**: [simplynixyn](https://github.com/SimNixyn)

---

## 🛡️ Overview

QDF Patrol Companion is a Python-based companion tool for Roblox QDF operatives that provides:

- Real-time DMR temperature/status monitoring via F9 log scraping.
- Advanced integrity degradation simulations.
- Intelligent estimation logic.

---

## ⚠️ Notices

> ❗ **Restricted Use**: This script includes antitamper mechanisms and will **only run if you are a member of the QDF Roblox group**. Unauthorized use triggers deterrent responses and exits execution.  
>
> ❗ **Data Disclaimer**: All data presented, including temperature readings, integrity estimations, and meltdown predictions, is derived from in-game logs and estimation algorithms. **This data is not guaranteed to be 100% accurate**. It is provided for general operational awareness only.
>
> ❗ **SOON TO BE PATCHED!**: This system's core functionality runs on QSERF's F9 Logs telemetry, and the devs has offically stated that they will be bringing it to end-of-life (likely within the next few QSERF combat patches) due to this tool utilzing these telemetry logs for purely unintended reasons that may give the QDF Operator in question a very very slight advantage. Since this tool has gotten moderation approval for use, it is not considered as a "cheat" or "exploit" that can be moderateable for, therefor why they're removing telemetry instead of attempting to outlaw this tool. So use this tool while you can and enjoy being able to see the DMR status anywhere at any time.
> 
> ❗ **Runtime Disclaimer**: While this python based tool has been compiled into a binary (.exe) for ease of use (plug-and-play), there will be a uncompiled version provided (not including .mp3s or any other optional assets) for peace of mind. Since as you know, never trust a random stranger on the internet offering you a unsigned binary. 

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

- Windows 7, 8, 10, 11+.
