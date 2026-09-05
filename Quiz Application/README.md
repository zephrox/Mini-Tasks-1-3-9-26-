# Quiz Application

A simple desktop Quiz Application built with Python and Tkinter. The app loads questions from a JSON file, allows question navigation, calculates scores, displays results, and saves score history.

---

## Features

- **Main Menu**: Landing screen with options to Start Quiz, View Score History, or Exit.
- **Question Navigation**: Move forward (`Next >`) and backward (`< Previous`) between questions. Your previous answers are preserved if you go back.
- **Back Navigation**: Dedicated `< Back to Menu` buttons across all pages for easy navigation.
- **Score Calculation & Results**: Displays final score, percentage, and pass/fail status upon completion.
- **Score History**: Automatically saves quiz attempts with timestamps, scores, and percentages to `scores.json`.
- **Clean UI**: Uses standard system fonts and native Tkinter controls without emoji dependencies to ensure consistent rendering across all machines.

---

## Project Structure

```
Quiz Application/
│
├── quiz_app.py         # Main application script (logic + Tkinter GUI)
├── questions.json      # Question bank file
├── scores.json         # Score history file (generated automatically)
└── README.md           # Project documentation
```

---

## Prerequisites

- **Python 3.7+**
- No external libraries required (uses standard library modules: `tkinter`, `json`, `os`, `datetime`).

---

## How to Run

1. Open your terminal or command prompt in the project directory:
   ```bash
   cd "path/to/Quiz Application"
   ```

2. Run the application:
   ```bash
   python quiz_app.py
   ```

---

## Adding New Questions

You can customize or add new questions by editing [questions.json](questions.json) using the following format:

```json
[
  {
    "question": "What is the capital of France?",
    "options": ["Paris", "London", "Berlin", "Madrid"],
    "answer": "Paris"
  }
]
```
