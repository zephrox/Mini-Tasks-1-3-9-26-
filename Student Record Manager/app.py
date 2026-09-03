"""
app.py - Lightweight Student Record Manager
Handles CRUD operations, JSON persistence, and search.
"""

import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student-records-secret"

DATA_FILE = os.path.join(os.path.dirname(__file__), "students.json")


# --- Data Persistence ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sid, s in data.items():
                if "id" not in s:
                    s["id"] = sid
            return data
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# --- Routes ---
@app.route("/")
def index():
    """Home / Student List with optional search filter."""
    query = request.args.get("q", "").strip()
    records = load_data()
    students = list(records.values())

    if query:
        q_lower = query.lower()
        students = [
            s for s in students
            if q_lower in str(s.get("id", "")).lower() or q_lower in str(s.get("name", "")).lower()
        ]

    students.sort(key=lambda s: str(s.get("id", "")))
    return render_template("index.html", students=students, query=query)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Add a new student record."""
    if request.method == "POST":
        sid = request.form.get("id", "").strip()
        name = request.form.get("name", "").strip()
        dept = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        form_data = {"id": sid, "name": name, "department": dept, "email": email, "phone": phone}

        # Validation
        if not all([sid, name, dept, email]):
            flash("Please fill in all required fields.", "error")
            return render_template("form.html", student=None, form_data=form_data)

        records = load_data()
        if sid in records:
            flash(f"Student ID '{sid}' already exists.", "error")
            return render_template("form.html", student=None, form_data=form_data)

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            flash("Please enter a valid email address.", "error")
            return render_template("form.html", student=None, form_data=form_data)

        records[sid] = {"id": sid, "name": name, "department": dept, "email": email, "phone": phone}
        save_data(records)
        flash(f"Student '{name}' added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", student=None, form_data=None)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_student(id):
    """Edit an existing student record."""
    records = load_data()
    student = records.get(str(id))

    if not student:
        flash("Student record not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dept = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if not all([name, dept, email]):
            flash("Please fill in all required fields.", "error")
            return render_template("form.html", student={"id": id, "name": name, "department": dept, "email": email, "phone": phone})

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            flash("Please enter a valid email address.", "error")
            return render_template("form.html", student={"id": id, "name": name, "department": dept, "email": email, "phone": phone})

        records[str(id)] = {"id": id, "name": name, "department": dept, "email": email, "phone": phone}
        save_data(records)
        flash(f"Student '{name}' updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", student=student, form_data=None)


@app.route("/delete/<id>")
def delete_student(id):
    """Delete a student record and redirect."""
    records = load_data()
    if str(id) in records:
        name = records[str(id)].get("name", id)
        del records[str(id)]
        save_data(records)
        flash(f"Student '{name}' deleted.", "success")
    else:
        flash("Student record not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
