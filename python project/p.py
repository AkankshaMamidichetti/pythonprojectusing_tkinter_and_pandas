import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os

# ---------------- FILE SETUP ----------------

FILE = "expenses.csv"

# Create CSV if it does not exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE, index=False)

# ---------------- FUNCTIONS ----------------

def update_text_area(content):
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, content)
    text_box.config(state="disabled")


def add_expense_gui():
    date = date_entry.get().strip()
    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
        return

    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    note = note_entry.get().strip()

    if amount == "":
        messagebox.showerror("Error", "Amount cannot be empty!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount!")
        return

    new_data = pd.DataFrame(
        [[date, category, amount, note]],
        columns=["Date", "Category", "Amount", "Note"]
    )

    new_data.to_csv(FILE, mode="a", header=False, index=False)

    messagebox.showinfo("Success", "Expense added successfully!")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)


def view_expenses_gui():
    df = pd.read_csv(FILE)
    if df.empty:
        update_text_area("No expenses recorded.")
    else:
        update_text_area(df.to_string(index=False))


def monthly_total_gui():
    df = pd.read_csv(FILE)

    # Handle mixed date formats safely
    df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["Date"])

    if df.empty:
        update_text_area("No valid date data available.")
        return

    df["Month"] = df["Date"].dt.to_period("M")
    total = df.groupby("Month")["Amount"].sum()

    update_text_area(total.to_string())


def category_total_gui():
    df = pd.read_csv(FILE)
    if df.empty:
        update_text_area("No data available.")
        return

    total = df.groupby("Category")["Amount"].sum()
    update_text_area(total.to_string())


def top_expenses_gui():
    df = pd.read_csv(FILE)
    if df.empty:
        update_text_area("No data available.")
        return

    top5 = df.nlargest(5, "Amount")
    update_text_area(top5.to_string(index=False))


def export_analysis_gui():
    df = pd.read_csv(FILE)

    df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["Date"])

    if df.empty:
        messagebox.showerror("Error", "No valid data to export")
        return

    df["Month"] = df["Date"].dt.to_period("M")

    summary = {
        "Monthly Total": df.groupby("Month")["Amount"].sum(),
        "Category Total": df.groupby("Category")["Amount"].sum()
    }

    summary_df = pd.concat(summary, axis=1)
    summary_df.to_csv("expense.csv")

    messagebox.showinfo("Export Complete", "Saved as 'expense.csv'")


# ---------------- UI ----------------

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")

title_label = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Category:").grid(row=1, column=0, padx=5)
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1, padx=5)

tk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1, padx=5)

tk.Label(frame, text="Note:").grid(row=3, column=0, padx=5)
note_entry = tk.Entry(frame)
note_entry.grid(row=3, column=1, padx=5)

add_btn = tk.Button(root, text="Add Expense", width=20, command=add_expense_gui)
add_btn.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="View All Expenses", width=20, command=view_expenses_gui).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Monthly Total", width=20, command=monthly_total_gui).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Category Total", width=20, command=category_total_gui).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Top 5 Expenses", width=20, command=top_expenses_gui).grid(row=1, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Export Analysis", width=20, command=export_analysis_gui).grid(row=1, column=1, padx=10, pady=10)

# Output Text Box
text_box = tk.Text(root, height=15, width=80, font=("Courier", 10))
text_box.pack(pady=20)
text_box.config(state="disabled")

root.mainloop()
