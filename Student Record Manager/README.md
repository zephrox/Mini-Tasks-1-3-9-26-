# Student Record Manager (Lightweight Edition)

A clean, minimal, and lightweight web application built with **Flask** and plain **HTML/CSS**.

---

## 📁 Trimmed Project Structure

Everything is condensed into just **5 files**:

```
Student Record Manager/
├── app.py                       # Single backend file (CRUD routes, validation, JSON storage)
├── students.json                # Local JSON persistent data store
├── static/
│   └── css/
│       └── style.css            # Lightweight minimal stylesheet (~160 lines)
└── templates/
    ├── base.html                # Clean navbar, alerts, and container (~30 lines)
    ├── index.html               # Combined List, Search, and Delete (~60 lines)
    └── form.html                # Unified Add & Edit form (~65 lines)
```

---

## ✨ Features & Simplifications

1. **Unified `form.html`**: Handles both adding a new student and editing an existing student with a simple `{% if student %}` condition.
2. **Integrated `index.html`**: Search bar and student listing live on the same page. Searching filters the table immediately without a separate search page.
3. **One-Click Delete**: Confirmation uses a clean native browser dialog (`onclick="return confirm(...)"`) — no extra modal template needed.
4. **All-in-One `app.py`**: Merged data helpers, routes, and validation into one clean ~80-line Python script.

---

## 🚀 How to Run

1. Install Flask:
   ```bash
   pip install flask
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open in browser: `http://localhost:5000`
