
# 📸 Snap Score Booster – Automate Snapchat Snaps

Boost your Snapchat score by automating the process of sending snaps using this simple Python tool.  
Designed for educational purposes.

---

## ⚙️ Features

- Auto-send snaps with custom intervals
- Simulate clicks at calibrated screen positions
- Update live progress in terminal
- Customizable settings
- Color-coded CLI interface

---

## 📦 Requirements

Python 3.10+ installed.

> You can install all dependencies automatically using the included `Install Requirements.bat` file.

---

## 🖥️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/snap-score-booster.git
cd snap-score-booster
```

### 2. Calibrate Screen Positions

Run the position calibrator first:

```bash
python getPosition.py
```

- A fullscreen window will appear.
- **Drag a box** over the camera interface on Snapchat.
- Confirm your selection (`y`) when asked.

This will generate a file: `ButtonPosition.json` with coordinates for auto-clicking.

---

### 3. Start the Snap Sender

Once calibration is done,run.bat or use the following:

```bash
python main.py
```
You will be asked:

- **Number of snaps** to send  
- **Interval** between snaps (seconds)  
- **Delay** between each button click

The tool will then start sending snaps and display live updates in the terminal.

Press ESC AT any time to safely exit.

---

## ❗ Disclaimer

This tool is intended for **educational and personal use only**.  
Do not use it to spam or violate Snapchat’s terms of service.  
Use responsibly and at your own risk.

---

## 💡 Credits

- SLIDERzz.
