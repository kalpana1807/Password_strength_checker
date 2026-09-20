# 🔐 Password Security Suite Pro

Password Security Suite Pro is a desktop application built with Python and Tkinter designed to help users create, evaluate, and manage strong passwords. It evaluates password strength in real time, estimates brute-force cracking difficulty, and checks passwords against leaked databases using the HaveIBeenPwned API.

---

## ✨ Features

- **⚡ Real-Time Strength Evaluation:** Visual meter and feedback indicating password strength based on length, digits, casing, and special symbols.
- **⏱️ Crack-Time Estimator:** Calculates the estimated time required for a brute-force attack against modern hardware.
- **🔍 Data Breach Verification:** Securely queries the HaveIBeenPwned API using the **k-Anonymity model** (SHA-1 prefix hashing) to check if a password has appeared in known data breaches.
- **🎲 Customizable Password Generator:** Generate strong, random passwords with configurable length sliders and character selection (uppercase, numbers, symbols).
- **👁️ Usability Controls:** Toggle password visibility (Show/Hide) and copy generated passwords directly to the system clipboard.
- **💾 Local Storage:** Option to export and save passwords locally to a text file.

---

## 🛠️ Built With

- **Python 3**
- **Tkinter** (Graphical User Interface)
- **hashlib & urllib** (SHA-1 hashing and API requests)
- **re & math** (Regex validation and complexity calculations)

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your system.

### Installation & Execution
1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/password-security-suite.git](https://github.com/YOUR_USERNAME/password-security-suite.git)
