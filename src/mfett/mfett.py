import tkinter as tk
from tkinter import ttk
import os
import random
from datetime import datetime

# --- Configuration ---
IMAGE_DATA_SOURCE = [
    # Aaron
    ('images/anger_aaron.png', 'a', 'Anger'),
    ('images/sadness_aaron.png', 's', 'Sadness'),
    ('images/disgust_aaron.png', 'd', 'Disgust'),
    ('images/fear_aaron.png', 'f', 'Fear'),
    ('images/confusion_aaron.png', 'c', 'Confusion'),
    ('images/neutral_aaron.png', 'n', 'Neutral'),
    ('images/joy_aaron.png', 'j', 'Joy'),
    ('images/surprise_aaron.png', 'p', 'Surprise'),
    # Adam
    ('images/anger_adam.png', 'a', 'Anger'),
    ('images/sadness_adam.png', 's', 'Sadness'),
    ('images/disgust_adam.png', 'd', 'Disgust'),
    ('images/fear_adam.png', 'f', 'Fear'),
    ('images/confusion_adam.png', 'c', 'Confusion'),
    ('images/neutral_adam.png', 'n', 'Neutral'),
    ('images/joy_adam.png', 'j', 'Joy'),
    ('images/surprise_adam.png', 'p', 'Surprise'),
    # Alex
    ('images/anger_alex.png', 'a', 'Anger'),
    ('images/sadness_alex.png', 's', 'Sadness'),
    ('images/disgust_alex.png', 'd', 'Disgust'),
    ('images/fear_alex.png', 'f', 'Fear'),
    ('images/confusion_alex.png', 'c', 'Confusion'),
    ('images/neutral_alex.png', 'n', 'Neutral'),
    ('images/joy_alex.png', 'j', 'Joy'),
    ('images/surprise_alex.png', 'p', 'Surprise'),
    # Alice
    ('images/anger_alice.png', 'a', 'Anger'),
    ('images/sadness_alice.png', 's', 'Sadness'),
    ('images/disgust_alice.png', 'd', 'Disgust'),
    ('images/fear_alice.png', 'f', 'Fear'),
    ('images/confusion_alice.png', 'c', 'Confusion'),
    ('images/neutral_alice.png', 'n', 'Neutral'),
    ('images/joy_alice.png', 'j', 'Joy'),
    ('images/surprise_alice.png', 'p', 'Surprise'),
    # Anna
    ('images/anger_anna.png', 'a', 'Anger'),
    ('images/sadness_anna.png', 's', 'Sadness'),
    ('images/disgust_anna.png', 'd', 'Disgust'),
    ('images/fear_anna.png', 'f', 'Fear'),
    ('images/confusion_anna.png', 'c', 'Confusion'),
    ('images/neutral_anna.png', 'n', 'Neutral'),
    ('images/joy_anna.png', 'j', 'Joy'),
    ('images/surprise_anna.png', 'p', 'Surprise')
]

class EmotionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Flashcard Game")
        self.root.geometry("1100x950")
        self.root.configure(bg="#f0f2f5")
        
        if not os.path.exists("user_data"): os.makedirs("user_data")
        
        self.is_maximized = False
        self.flash_duration, self.difficulty_name = 100, "Hard"
        self.game_started = self.game_over = self.waiting_for_key = False
        self.index = 0

        # UI Header
        self.top_bar = tk.Frame(root, bg="#f0f2f5")
        self.top_bar.pack(fill="x", pady=10)
        
        ttk.Button(self.top_bar, text="Quit (Ctrl+q)", command=self.root.destroy).pack(side="right", padx=10)
        self.fs_btn = ttk.Button(self.top_bar, text="Toggle Fullscreen (Ctrl+f)", command=self.toggle_maximize)
        self.fs_btn.pack(side="right", padx=10)

        self.diff_label = tk.Label(self.top_bar, text=f"Difficulty: {self.difficulty_name}", 
                                  font=("Segoe UI Semibold", 14), bg="#f0f2f5", fg="#007bff")
        self.diff_label.pack(side="left", padx=20)

        # Main Card
        self.card = tk.Frame(root, bg="white", highlightthickness=1, highlightbackground="#ddd")
        self.card.pack(pady=10, padx=50, fill="both", expand=True)

        self.name_entry = tk.Entry(self.card, font=("Segoe UI", 16), justify="center")
        
        self.diff_btn_frame = tk.Frame(self.card, bg="white")
        ttk.Button(self.diff_btn_frame, text="Easy (E)", command=lambda: self.set_difficulty(500, "Easy")).pack(side="left", padx=5)
        ttk.Button(self.diff_btn_frame, text="Medium (M)", command=lambda: self.set_difficulty(250, "Medium")).pack(side="left", padx=5)
        ttk.Button(self.diff_btn_frame, text="Hard (H)", command=lambda: self.set_difficulty(100, "Hard")).pack(side="left", padx=5)

        self.start_btn = ttk.Button(self.card, text="START ROUND", command=self.start_or_next)
        self.clear_stats_btn = ttk.Button(self.card, text="Clear Stats (Backup)", command=self.backup_and_clear)
        
        self.label = tk.Label(self.card, text="", font=("Segoe UI", 14), bg="white", justify="center")
        self.label.pack(pady=10)

        self.image_label = tk.Label(self.card, bg="white")
        self.image_label.pack(fill="both", expand=True)

        self.chart_canvas = tk.Canvas(self.card, width=400, height=120, bg="white", highlightthickness=0)
        
        self.replay_btn = ttk.Button(self.card, text="Replay Image (R)", command=self.show_flashcard)
        self.reset_btn = ttk.Button(self.card, text="Play Again (ENTER)", command=self.reset_game)

        # Bindings
        self.root.bind("<Control-f>", lambda e: self.toggle_maximize())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())
        self.root.bind("<space>", self.handle_space)
        self.root.bind("r", lambda e: self.handle_replay_key())
        self.root.bind("<Return>", lambda e: self.handle_enter())
        self.root.bind("<Button-1>", self.on_click_anywhere)
        
        self.root.bind("e", lambda e: self.set_difficulty(500, "Easy") if self.root.focus_get() != self.name_entry else None)
        self.root.bind("m", lambda e: self.set_difficulty(250, "Medium") if self.root.focus_get() != self.name_entry else None)
        self.root.bind("h", lambda e: self.set_difficulty(100, "Hard") if self.root.focus_get() != self.name_entry else None)
        
        for _, key, _ in IMAGE_DATA_SOURCE:
            self.root.bind(key, self.check_answer)

        self.reset_game()

    def on_click_anywhere(self, event):
        if event.widget != self.name_entry: self.root.focus_set()

    def toggle_maximize(self):
        self.is_maximized = not self.is_maximized
        try: self.root.state("zoomed" if self.is_maximized else "normal")
        except: self.root.attributes("-zoomed", self.is_maximized)

    def backup_and_clear(self):
        name = self.name_entry.get().strip() or "Anonymous"
        file_path = os.path.join("user_data", f"{name}.txt")
        if os.path.exists(file_path):
            date_str = datetime.now().strftime("%Y%m%d")
            new_path = os.path.join("user_data", f"{date_str}_{name}.bak")
            os.rename(file_path, new_path)
            self.chart_canvas.delete("all")
            self.chart_canvas.pack_forget()
            if self.game_over: self.label.config(text="Stats Cleared and Backed Up!\nPress ENTER to play again.")

    def set_difficulty(self, duration, name):
        if not self.game_started or self.game_over:
            self.flash_duration, self.difficulty_name = duration, name
            self.diff_label.config(text=f"Difficulty: {self.difficulty_name}")

    def reset_game(self):
        self.current_data = list(IMAGE_DATA_SOURCE)
        random.shuffle(self.current_data)
        self.index = 0
        self.game_started = self.game_over = self.waiting_for_key = False
        self.stats = {name: {'correct': 0, 'total': 0} for _, _, name in IMAGE_DATA_SOURCE}
        self.reset_btn.pack_forget()
        self.chart_canvas.pack_forget()
        self.clear_stats_btn.pack_forget()
        
        self.name_entry.pack(pady=5)
        self.diff_btn_frame.pack(pady=5)
        self.start_btn.pack(pady=5)
        self.clear_stats_btn.pack(pady=5) # Added to Start Screen
        self.label.config(text="Set Difficulty & Press Start", font=("Segoe UI", 18), fg="black")

    def handle_space(self, event):
        if self.root.focus_get() == self.name_entry:
            self.start_or_next(); return "break"
        self.start_or_next()

    def start_or_next(self):
        if self.game_over or self.waiting_for_key: return
        if not self.game_started:
            self.user_name = self.name_entry.get().strip() or "Anonymous"
            self.name_entry.pack_forget(); self.start_btn.pack_forget()
            self.diff_btn_frame.pack_forget(); self.clear_stats_btn.pack_forget()
            self.root.focus_set()
        self.game_started = True
        self.show_flashcard()

    def show_flashcard(self):
        if self.index >= len(self.current_data): return
        self.replay_btn.pack_forget()
        self.waiting_for_key = False 
        img_path, _, _ = self.current_data[self.index]
        self.img = tk.PhotoImage(file=img_path)
        self.image_label.config(image=self.img)
        self.label.config(text="Look...")
        self.root.after(self.flash_duration, self.hide_flashcard)

    def hide_flashcard(self):
        self.image_label.config(image='')
        self.label.config(text="Identify the emotion\n(a/s/d/f/c/n/j/p)")
        self.waiting_for_key = True
        self.replay_btn.pack(pady=10)

    def check_answer(self, event):
        if not self.waiting_for_key or self.root.focus_get() == self.name_entry: return
        self.replay_btn.pack_forget()
        _, correct_key, emotion_name = self.current_data[self.index]
        self.stats[emotion_name]['total'] += 1
        if event.char == correct_key:
            self.stats[emotion_name]['correct'] += 1
            self.label.config(text="CORRECT", fg="green")
        else:
            self.label.config(text=f"WRONG ({emotion_name})", fg="red")
        self.waiting_for_key = False
        self.index += 1
        if self.index < len(self.current_data):
            self.root.after(1000, lambda: self.label.config(text="Press SPACE for next", fg="black"))
        else:
            self.root.after(1000, self.save_data_and_report)

    def draw_chart(self, scores):
        self.chart_canvas.delete("all")
        if not scores: return
        w, h, max_score, padding = 400, 120, len(IMAGE_DATA_SOURCE), 20
        self.chart_canvas.create_line(padding, h-padding, w-padding, h-padding, fill="gray")
        self.chart_canvas.create_line(padding, padding, padding, h-padding, fill="gray")
        if len(scores) < 2: return
        x_step = (w - 2*padding) / (len(scores) - 1)
        y_scale = (h - 2*padding) / max_score
        points = []
        for i, val in enumerate(scores):
            x, y = padding + (i * x_step), (h - padding) - (val * y_scale)
            points.extend([x, y])
            self.chart_canvas.create_oval(x-2, y-2, x+2, y+2, fill="#007bff")
        self.chart_canvas.create_line(points, fill="#007bff", width=2, smooth=True)

    def save_data_and_report(self):
        self.game_over = True; self.label.config(fg="black"); self.replay_btn.pack_forget()
        total_correct = sum(d['correct'] for d in self.stats.values())
        session_log = [f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"Difficulty: {self.difficulty_name}"]
        for n, d in self.stats.items(): session_log.append(f"{n}: {d['correct']}/{d['total']}")
        session_log.append(f"Final Score: {total_correct}/{len(IMAGE_DATA_SOURCE)}")
        
        file_path = os.path.join("user_data", f"{self.user_name}.txt")
        with open(file_path, "a") as f: f.write("\n".join(session_log) + "\n" + "-"*30 + "\n")
        
        all_scores = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    if "Final Score:" in line:
                        try: all_scores.append(int(line.split(":")[-1].split("/")[0].strip()))
                        except: pass
        avg = sum(all_scores)/len(all_scores) if all_scores else 0
        
        # Performance Text
        report = f"GAME OVER\nScore: {total_correct}/{len(IMAGE_DATA_SOURCE)}\nSessions: {len(all_scores)} | Avg: {avg:.1f}"
        self.label.config(text=report)
        
        # Display Chart and Controls
        self.chart_canvas.pack(pady=5); self.draw_chart(all_scores)
        self.reset_btn.pack(pady=5)
        self.clear_stats_btn.pack(pady=5) # Added to End Screen

    def handle_enter(self):
        if self.game_over: self.reset_game()
    def handle_replay_key(self):
        if self.waiting_for_key: self.show_flashcard()

if __name__ == "__main__":
    root = tk.Tk()
    game = EmotionGame(root)
    root.mainloop()
