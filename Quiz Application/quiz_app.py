import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

# File paths resolved relative to the script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")


def load_questions(file_path):
    """Loads questions from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find questions file:\n{file_path}")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to parse JSON questions file.")
        return []


def save_score(score, total, file_path):
    """Saves a completed quiz score to a valid JSON history list."""
    history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    history = data
        except (json.JSONDecodeError, IOError):
            history = []

    percentage = round((score / total) * 100, 1) if total > 0 else 0.0
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total": total,
        "percentage": percentage
    })

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except IOError as e:
        messagebox.showerror("Error", f"Failed to save score history: {e}")


def load_score_history(file_path):
    """Loads previous score attempts from the history JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, IOError):
            return []
    return []


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("560x440")
        self.root.resizable(False, False)

        self.questions = []
        self.current_index = 0
        self.user_answers = {}
        self.selected_option = tk.StringVar()

        # Main container that swaps screen contents
        self.container = tk.Frame(self.root, padx=25, pady=20)
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def clear_screen(self):
        """Clears all widgets inside the container frame."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # ------------------ Screen: Main Menu ------------------
    def show_main_menu(self):
        """Renders the landing main menu screen."""
        self.clear_screen()

        title_lbl = tk.Label(
            self.container,
            text="Quiz Application",
            font=("Helvetica", 18, "bold"),
            fg="#1F2937"
        )
        title_lbl.pack(pady=(35, 10))

        subtitle_lbl = tk.Label(
            self.container,
            text="Welcome! Choose an option below to get started.",
            font=("Helvetica", 11),
            fg="#4B5563"
        )
        subtitle_lbl.pack(pady=(0, 35))

        btn_frame = tk.Frame(self.container)
        btn_frame.pack()

        btn_start = tk.Button(
            btn_frame,
            text="Start Quiz",
            font=("Helvetica", 11, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            width=22,
            pady=8,
            cursor="hand2",
            command=self.start_quiz
        )
        btn_start.pack(pady=6)

        btn_history = tk.Button(
            btn_frame,
            text="View Score History",
            font=("Helvetica", 11),
            width=22,
            pady=8,
            cursor="hand2",
            command=self.show_history
        )
        btn_history.pack(pady=6)

        btn_exit = tk.Button(
            btn_frame,
            text="Exit",
            font=("Helvetica", 11),
            width=22,
            pady=8,
            cursor="hand2",
            command=self.root.quit
        )
        btn_exit.pack(pady=6)

    # ------------------ Screen: Quiz Questions ------------------
    def start_quiz(self):
        """Initializes quiz state and begins question presentation."""
        self.questions = load_questions(QUESTIONS_FILE)
        if not self.questions:
            return

        self.current_index = 0
        self.user_answers = {}
        self.display_question()

    def display_question(self):
        """Renders the question at current_index with back/next navigation."""
        self.clear_screen()

        total = len(self.questions)
        question_data = self.questions[self.current_index]

        # Top navigation / status bar
        top_bar = tk.Frame(self.container)
        top_bar.pack(fill="x", pady=(0, 15))

        btn_back_menu = tk.Button(
            top_bar,
            text="< Back to Menu",
            font=("Helvetica", 9),
            command=self.confirm_back_to_menu
        )
        btn_back_menu.pack(side="left")

        progress_lbl = tk.Label(
            top_bar,
            text=f"Question {self.current_index + 1} of {total}",
            font=("Helvetica", 10, "bold"),
            fg="#4B5563"
        )
        progress_lbl.pack(side="right")

        # Question prompt
        question_lbl = tk.Label(
            self.container,
            text=question_data["question"],
            font=("Helvetica", 13, "bold"),
            wraplength=490,
            justify="left"
        )
        question_lbl.pack(anchor="w", pady=(5, 15))

        # Restore previously selected option if user navigated back
        previous_choice = self.user_answers.get(self.current_index, "")
        self.selected_option.set(previous_choice)

        # Options frame
        options_frame = tk.Frame(self.container)
        options_frame.pack(fill="x", pady=5)

        for option in question_data["options"]:
            rb = tk.Radiobutton(
                options_frame,
                text=option,
                value=option,
                variable=self.selected_option,
                font=("Helvetica", 11),
                anchor="w",
                padx=5,
                pady=4,
                cursor="hand2"
            )
            rb.pack(fill="x", anchor="w")

        # Bottom navigation buttons: [Previous Question] and [Next / Submit]
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(fill="x", pady=(25, 0))

        if self.current_index > 0:
            btn_prev = tk.Button(
                nav_frame,
                text="< Previous",
                font=("Helvetica", 10),
                padx=12,
                pady=5,
                command=self.handle_previous
            )
            btn_prev.pack(side="left")

        is_last = self.current_index == total - 1
        next_text = "Submit Quiz" if is_last else "Next >"
        btn_next = tk.Button(
            nav_frame,
            text=next_text,
            font=("Helvetica", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            padx=16,
            pady=5,
            command=self.handle_next
        )
        btn_next.pack(side="right")

    def handle_previous(self):
        """Saves current selection and moves to the previous question."""
        if self.selected_option.get():
            self.user_answers[self.current_index] = self.selected_option.get()

        if self.current_index > 0:
            self.current_index -= 1
            self.display_question()

    def handle_next(self):
        """Validates selection, stores answer, and advances question or finishes."""
        user_choice = self.selected_option.get().strip()
        if not user_choice:
            messagebox.showwarning("Selection Required", "Please select an answer before continuing.")
            return

        self.user_answers[self.current_index] = user_choice

        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.display_question()
        else:
            self.show_results()

    def confirm_back_to_menu(self):
        """Asks confirmation before exiting an active quiz session."""
        if messagebox.askyesno("Exit Quiz", "Are you sure you want to return to the Main Menu? Your progress will be lost."):
            self.show_main_menu()

    # ------------------ Screen: Results ------------------
    def show_results(self):
        """Calculates score, displays results, saves history, and offers navigation."""
        self.clear_screen()

        total = len(self.questions)
        score = sum(
            1 for idx, q in enumerate(self.questions)
            if self.user_answers.get(idx) == q["answer"]
        )
        percentage = round((score / total) * 100, 1) if total > 0 else 0.0
        passed = percentage >= 50.0

        # Save score to history file
        save_score(score, total, SCORES_FILE)

        title_lbl = tk.Label(
            self.container,
            text="Quiz Results",
            font=("Helvetica", 16, "bold"),
            fg="#1F2937"
        )
        title_lbl.pack(pady=(20, 10))

        score_lbl = tk.Label(
            self.container,
            text=f"Your Score: {score} / {total} ({percentage}%)",
            font=("Helvetica", 14)
        )
        score_lbl.pack(pady=5)

        status_text = "Status: Passed" if passed else "Status: Needs Improvement"
        status_color = "#16A34A" if passed else "#DC2626"
        status_lbl = tk.Label(
            self.container,
            text=status_text,
            font=("Helvetica", 12, "bold"),
            fg=status_color
        )
        status_lbl.pack(pady=8)

        # Action / navigation buttons
        btn_frame = tk.Frame(self.container)
        btn_frame.pack(pady=25)

        btn_retake = tk.Button(
            btn_frame,
            text="Retake Quiz",
            font=("Helvetica", 10, "bold"),
            bg="#2563EB",
            fg="white",
            padx=14,
            pady=5,
            command=self.start_quiz
        )
        btn_retake.pack(side="left", padx=6)

        btn_history = tk.Button(
            btn_frame,
            text="View History",
            font=("Helvetica", 10),
            padx=14,
            pady=5,
            command=self.show_history
        )
        btn_history.pack(side="left", padx=6)

        btn_menu = tk.Button(
            btn_frame,
            text="< Main Menu",
            font=("Helvetica", 10),
            padx=14,
            pady=5,
            command=self.show_main_menu
        )
        btn_menu.pack(side="left", padx=6)

    # ------------------ Screen: Score History ------------------
    def show_history(self):
        """Displays score history page with a Back to Menu button."""
        self.clear_screen()

        # Header bar
        header_bar = tk.Frame(self.container)
        header_bar.pack(fill="x", pady=(0, 10))

        btn_back = tk.Button(
            header_bar,
            text="< Back to Menu",
            font=("Helvetica", 9),
            command=self.show_main_menu
        )
        btn_back.pack(side="left")

        title_lbl = tk.Label(
            header_bar,
            text="Score History",
            font=("Helvetica", 14, "bold"),
            fg="#1F2937"
        )
        title_lbl.pack(side="left", padx=15)

        # History list container
        list_container = tk.Frame(self.container)
        list_container.pack(fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10)
        )
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        history = load_score_history(SCORES_FILE)
        if not history:
            listbox.insert(tk.END, "No previous quiz records found.")
        else:
            for idx, entry in enumerate(reversed(history), start=1):
                date = entry.get("date", "Unknown date")
                score = entry.get("score", 0)
                total = entry.get("total", 0)
                pct = entry.get("percentage", 0.0)
                status = "Passed" if pct >= 50.0 else "Failed"
                listbox.insert(tk.END, f"#{idx} | {date}")
                listbox.insert(tk.END, f"     Score: {score}/{total} ({pct}%) - {status}")
                listbox.insert(tk.END, "-" * 48)

        # Bottom Back button for easy navigation
        btn_bottom_back = tk.Button(
            self.container,
            text="< Back to Menu",
            font=("Helvetica", 10),
            padx=14,
            pady=5,
            command=self.show_main_menu
        )
        btn_bottom_back.pack(pady=(5, 0))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
