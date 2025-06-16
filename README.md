# maclinux_mint_kbd_fix
Fixing capslock wrongly mapping the keyboard

🧠 Automatically fixes broken key mappings caused by the Caps Lock key when using Apple (Mac) keyboards on Linux Mint (or other Debian-based distros).  
⚙️ Designed for Bluetooth and built-in Apple keyboards — works persistently across reboots and logins.

---

## 💡 Problem

When using an Apple Bluetooth or built-in keyboard on Linux, pressing **Caps Lock** may cause the keyboard layout to break — letters become numbers or special characters (e.g., typing `qwertyuiop` results in `qwerty456`). 
This issue can occur on iMacs or MacBooks running Linux Mint, Debian, or similar distributions.

## ✅ Solution

This tool continuously monitors for the Apple keyboard and automatically reapplies a known-good fix whenever Caps Lock causes the layout to break. 
It works seamlessly in the background via a `systemd --user` service.

---

## 📦 Features

- Detects the Apple keyboard device path dynamically (`/dev/input/eventX`)
- Automatically grabs and releases the keyboard input using `evtest` to restore correct layout
- Runs at login using a user systemd service
- Restarts automatically if the keyboard is temporarily unavailable

---

## 🛠 Installation


### 1. Clone this repo

```bash
git clone https://github.com/Kamsam-Samkam/maclinux_mint_kbd_fix.git
cd capslock_autofix.py
