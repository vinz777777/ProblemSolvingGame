import tkinter as tk
from tkinter import ttk, messagebox
import random, json, os

# === Setup Leaderboard Directory ===
LEADERBOARD_DIR = "leaderboard"
os.makedirs(LEADERBOARD_DIR, exist_ok=True)
LEADERBOARD_FILE = os.path.join(LEADERBOARD_DIR, "scores.json")

# === Leaderboard Functions ===
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

# === Game Logic ===
def generate_problem(level):
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"{a} + {b} = ?", a + b
    elif level == 2:
        a, b = random.randint(10, 50), random.randint(10, 50)
        return f"{a} - {b} = ?", a - b
    else:
        a, b = random.randint(2, 12), random.randint(2, 12)
        return f"{a} × {b} = ?", a * b

# === Main Game Class ===
class ProblemSolvingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧩 Problem-Solving Skills Game")
        self.geometry("800x600")
        self.configure(bg="#0d1117")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#0d1117", borderwidth=0)
        style.configure("TNotebook.Tab", background="#161b22", foreground="#58a6ff",
                        font=("Poppins", 12, "bold"), padding=(15, 8))
        style.map("TNotebook.Tab", background=[("selected", "#1f6feb")], foreground=[("selected", "white")])

        # Game Variables
        self.player_name = ""
        self.score = 0
        self.xp = 0
        self.level = 1
        self.current_problem = ""
        self.correct_answer = 0

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.menu_tab = ttk.Frame(self.notebook, style="TFrame")
        self.game_tab = ttk.Frame(self.notebook, style="TFrame")
        self.leaderboard_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.pack(expand=True, fill="both")

        self.create_menu_tab()
        self.create_game_tab()
        self.create_leaderboard_tab()

        self.notebook.add(self.menu_tab, text="🏠 Menu")
        self.notebook.add(self.game_tab, text="🎮 Game")
        self.notebook.add(self.leaderboard_tab, text="🏆 Leaderboard")

        self.show_menu()

    # === UI Building ===
    def create_menu_tab(self):
        frame = tk.Frame(self.menu_tab, bg="#0d1117")
        frame.pack(expand=True, fill="both")

        # Centered container for content
        container = tk.Frame(frame, bg="#0d1117")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="🧠 Problem-Solving Game",
            font=("Poppins", 32, "bold"),
            fg="#58a6ff",
            bg="#0d1117"
        ).pack(pady=30)

        tk.Label(
            container,
            text="Enter your name:",
            font=("Poppins", 16),
            fg="white",
            bg="#0d1117"
        ).pack(pady=10)

        self.name_entry = tk.Entry(
            container,
            font=("Poppins", 16),
            justify="center",
            width=25,
            bg="#161b22",
            fg="#58a6ff",
            insertbackground="#58a6ff",
            relief="flat",
        )
        self.name_entry.pack(pady=15)

        self.create_glow_button(container, "Start Game", "#238636", self.start_game).pack(pady=20)
        self.create_glow_button(
            container, "View Leaderboard", "#1f6feb",
            lambda: self.notebook.select(self.leaderboard_tab)
        ).pack(pady=10)

    def create_game_tab(self):
        frame = tk.Frame(self.game_tab, bg="#0d1117")
        frame.pack(expand=True, fill="both")

        self.info_label = tk.Label(frame, text="", font=("Poppins", 14), fg="white", bg="#0d1117")
        self.info_label.pack(pady=10)

        self.problem_label = tk.Label(frame, text="", font=("Poppins", 26, "bold"),
                                      fg="#58a6ff", bg="#0d1117")
        self.problem_label.pack(pady=40)

        self.answer_entry = tk.Entry(frame, font=("Poppins", 18), justify="center", width=10,
                                     bg="#161b22", fg="#58a6ff", insertbackground="#58a6ff", relief="flat")
        self.answer_entry.pack(pady=10)

        self.create_glow_button(frame, "Submit Answer", "#1f6feb", self.submit_answer).pack(pady=15)
        self.create_glow_button(frame, "End Game", "#d73a49", self.end_game).pack(pady=10)

        self.xp_label = tk.Label(frame, text="XP: 0", font=("Poppins", 12), fg="#8b949e", bg="#0d1117")
        self.xp_label.pack(pady=15)

    def create_leaderboard_tab(self):
        frame = tk.Frame(self.leaderboard_tab, bg="#0d1117")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="🏆 Top 10 Players 🏆",
                 font=("Poppins", 24, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=20)

        self.lb_frame = tk.Frame(frame, bg="#0d1117")
        self.lb_frame.pack()
        self.update_leaderboard()

        self.create_glow_button(frame, "↩ Back to Menu", "#238636", self.show_menu).pack(pady=25)

    # === Glow Button Factory ===
    def create_glow_button(self, parent, text, color, command):
        def on_enter(e): btn.config(bg=color, fg="white")
        def on_leave(e): btn.config(bg="#161b22", fg=color)
        btn = tk.Button(parent, text=text, font=("Poppins", 14, "bold"), width=20,
                        bg="#161b22", fg=color, activebackground=color, activeforeground="white",
                        relief="flat", cursor="hand2", command=command)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # === Core Functions ===
    def show_menu(self):
        self.notebook.select(self.menu_tab)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name to start.")
            return
        self.player_name = name
        self.score = 0
        self.xp = 0
        self.level = 1
        self.new_problem()
        self.notebook.select(self.game_tab)

    def new_problem(self):
        problem, answer = generate_problem(self.level)
        self.current_problem = problem
        self.correct_answer = answer
        self.info_label.config(text=f"👤 {self.player_name} | 💯 Score: {self.score} | 🧩 Level: {self.level}")
        self.problem_label.config(text=problem)
        self.answer_entry.delete(0, tk.END)
        self.xp_label.config(text=f"XP: {self.xp}/30")

    def submit_answer(self):
        answer = self.answer_entry.get().strip()

        # Validate integer input (accepts negative numbers)
        try:
            answer_int = int(answer)
        except ValueError:
            messagebox.showinfo("Invalid", "Please enter a valid integer.")
            return

        # Check if the answer is correct
        if answer_int == self.correct_answer:
            self.score += 10
            self.xp += 10
            if self.xp >= 30:
                self.level += 1
                self.xp = 0
                messagebox.showinfo("🎉 Level Up!", f"You're now on Level {self.level}!")
            self.new_problem()
        else:
            messagebox.showinfo("❌ Incorrect", f"The correct answer was {self.correct_answer}.")
            self.new_problem()

    def end_game(self):
        save_score(self.player_name, self.score)
        messagebox.showinfo("Game Over", f"Thanks for playing, {self.player_name}!\nYour final score: {self.score}")
        self.update_leaderboard()
        self.show_menu()

    def update_leaderboard(self):
        for widget in self.lb_frame.winfo_children():
            widget.destroy()

        scores = load_leaderboard()
        if not scores:
            tk.Label(self.lb_frame, text="No scores yet.", font=("Poppins", 14),
                     fg="#8b949e", bg="#0d1117").pack()
        else:
            for i, entry in enumerate(scores, 1):
                tk.Label(self.lb_frame,
                         text=f"{i}. {entry['name']} — {entry['score']} pts",
                         font=("Poppins", 14), fg="#c9d1d9", bg="#0d1117").pack(anchor="w", padx=180, pady=2)

# === Run Game ===
if __name__ == "__main__":
    app = ProblemSolvingGame()
    app.mainloop()
