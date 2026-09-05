import json
import os
import tkinter as tk
import calendar
from collections import defaultdict
from datetime import datetime
from tkinter import messagebox

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        messagebox.showerror("Error", "The expenses file could not be read.")
        return []


def save_expenses(expense_records):
    with open(DATA_FILE, "w") as file:
        json.dump(expense_records, file, indent=4)


def add_expense(amount, category, date):
    expense_records.append({"amount": amount, "category": category, "date": date})
    save_expenses(expense_records)
    update_listbox()


def delete_expense(index):
    if 0 <= index < len(expense_records):
        del expense_records[index]
        save_expenses(expense_records)
        update_listbox()
    else:
        messagebox.showerror("Error", "Invalid expense index.")


def add_expense_gui():
    amount_text = amount_entry.get().strip()
    category = category_entry.get().strip()
    date = date_entry.get().strip()

    if not amount_text or not category or not date:
        messagebox.showerror("Error", "Amount, category, and date are required.")
        return

    try:
        amount = float(amount_text)
        datetime.strptime(date, "%Y-%m-%d")
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a positive amount and a date in YYYY-MM-DD format.")
        return

    add_expense(amount, category, date)
    clear_entries()


def delete_expense_gui():
    selected_index = expenses_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "No expense selected.")
        return
    delete_expense(selected_index[0])


def update_listbox():
    expenses_listbox.delete(0, tk.END)
    for expense in expense_records:
        expenses_listbox.insert(
            tk.END,
            f"{expense['date']}: ${expense['amount']:.2f} - {expense['category']}",
        )


def show_category_totals():
    if not expense_records:
        messagebox.showinfo("Category Totals", "No expenses recorded.")
        return
    totals = defaultdict(float)
    for expense in expense_records:
        totals[expense["category"]] += expense["amount"]
    report = "\n".join(f"{category}: ${total:.2f}" for category, total in sorted(totals.items()))
    report += f"\n\nOverall total: ${sum(totals.values()):.2f}"
    messagebox.showinfo("Category Totals", report)


def show_monthly_totals():
    if not expense_records:
        messagebox.showinfo("Monthly Totals", "No expenses recorded.")
        return
    totals = defaultdict(float)
    for expense in expense_records:
        month = expense["date"][:7]
        totals[month] += expense["amount"]
    report = "\n".join(f"{month}: ${total:.2f}" for month, total in sorted(totals.items()))
    messagebox.showinfo("Monthly Totals", report)


def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


def show_date_picker():
    today = datetime.today()
    try:
        selected_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
    except ValueError:
        selected_date = today

    picker = tk.Toplevel(root)
    picker.title("Choose Date")
    picker.resizable(False, False)
    picker.transient(root)
    picker.grab_set()

    month = selected_date.month
    year = selected_date.year
    header = tk.Frame(picker)
    header.pack(padx=8, pady=8)
    calendar_frame = tk.Frame(picker)
    calendar_frame.pack(padx=8, pady=(0, 8))

    def change_month(amount):
        nonlocal month, year
        month += amount
        if month == 0:
            month, year = 12, year - 1
        elif month == 13:
            month, year = 1, year + 1
        render_calendar()

    def choose_date(day):
        date_entry.delete(0, tk.END)
        date_entry.insert(0, f"{year:04d}-{month:02d}-{day:02d}")
        picker.destroy()

    def render_calendar():
        for widget in header.winfo_children():
            widget.destroy()
        for widget in calendar_frame.winfo_children():
            widget.destroy()

        tk.Button(header, text="<", width=3, command=lambda: change_month(-1)).grid(row=0, column=0)
        tk.Label(header, text=f"{calendar.month_name[month]} {year}", width=18).grid(row=0, column=1)
        tk.Button(header, text=">", width=3, command=lambda: change_month(1)).grid(row=0, column=2)

        for column, weekday in enumerate(calendar.day_abbr):
            tk.Label(calendar_frame, text=weekday, width=4).grid(row=0, column=column)
        for row, week in enumerate(calendar.monthcalendar(year, month), start=1):
            for column, day in enumerate(week):
                if day:
                    tk.Button(
                        calendar_frame,
                        text=str(day),
                        width=4,
                        command=lambda day=day: choose_date(day),
                    ).grid(row=row, column=column, padx=1, pady=1)

    render_calendar()


expense_records = load_expenses()
root = tk.Tk()
root.title("Expense Tracker")
tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Choose Date", command=show_date_picker).grid(row=2, column=2, padx=10, pady=5)
tk.Button(root, text="Add Expense", command=add_expense_gui).grid(row=3, column=0, columnspan=2, padx=10, pady=5)
tk.Button(root, text="Delete Expense", command=delete_expense_gui).grid(row=4, column=0, columnspan=2, padx=10, pady=5)
tk.Button(root, text="Category Totals", command=show_category_totals).grid(row=5, column=0, padx=10, pady=5)
tk.Button(root, text="Monthly Totals", command=show_monthly_totals).grid(row=5, column=1, padx=10, pady=5)
expenses_listbox = tk.Listbox(root, width=50, height=10)
expenses_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
update_listbox()
root.mainloop()