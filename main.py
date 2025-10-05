import tkinter as tk
import pygame
import random
import math
import os

FONT_PATH = "game_font.ttf"

game_levels = [
    {
        "story": "A terrorist demands you kill one innocent child or they'll detonate a bomb killing thousands. Will you take one life to save many?",
        "choices": ["Kill one", "Refuse"]
    },
    {
        "story": "Would you rather go to DayDream event at IIT Delhi by leaving your JEE classes which will create a backlog?",
        "choices": ["Yes, I will", "No, preparation is important"]
    },
    {
        "story": "A scientist offers to erase your most painful memory — but it also means forgetting the person who shaped your strength.",
        "choices": ["Erase it", "Keep it"]
    },
    {
        "story": "Your dying sibling can be saved if you clone and harvest organs from the clone — but the clone is conscious.",
        "choices": ["Use the clone", "Refuse"]
    },
    {
        "story": "You can travel back and stop a tragedy — but that act will erase your own existence. Will you die for a world that never knew you?",
        "choices": ["Go back", "Stay"]
    },
    {
        "story": "You are given control over life and death. You can eliminate all pain in the world, but free will will vanish. Do you create a perfect but controlled world?",
        "choices": ["Press the switch", "Refuse"]
    }
]


class InterstellarGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Interstellar Decision Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#000010")
        self.root.resizable(False, False)

        # Reward / moral points
        self.moral_points = 0

        # Initialize pygame mixer for background music
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("audiogame.mp3")  # Replace with your music file
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Could not load music:", e)

        # Load fonts
        if os.path.exists(FONT_PATH):
            import tkinter.font as tkFont
            self.custom_font = tkFont.Font(file=FONT_PATH, size=16)
            self.header_font = tkFont.Font(file=FONT_PATH, size=36, weight="bold")
            self.subheader_font = tkFont.Font(file=FONT_PATH, size=20, slant="italic")
        else:
            self.custom_font = ("Courier New", 16, "bold")
            self.header_font = ("Courier New", 36, "bold")
            self.subheader_font = ("Courier New", 20, "italic")

        # Canvas for background animations
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0, bg="#000010")
        self.canvas.place(x=0, y=0)

        self.starfield = []
        self.create_starfield(150)

        self.nebula_circles = []
        self.create_nebula()

        # Header
        self.header_text = "== CHOOSE YOUR PATH =="
        self.header = tk.Label(root, text=self.header_text, bg="#000010",
                               fg="#99d9ff", font=self.header_font)
        self.header.place(relx=0.5, y=40, anchor="center")

        self.subheader_text = "Sacrifices Must Be Made"
        self.subheader = tk.Label(root, text=self.subheader_text, bg="#000010",
                                  fg="#66bbff", font=self.subheader_font)
        self.subheader.place(relx=0.5, y=90, anchor="center")

        # Text area
        self.text_frame_bg = tk.Frame(root, bg="#0a0a1a", bd=0)
        self.text_frame_bg.place(x=50, y=130, width=700, height=260)

        self.text_frame = tk.Frame(self.text_frame_bg, bg="#101025")
        self.text_frame.pack(fill="both", expand=True, padx=3, pady=3)

        self.glow_frames = []
        glow_colors = ["#223355", "#335577", "#446688"]
        for i, color in enumerate(glow_colors):
            f = tk.Frame(root, bg=color)
            f.place(x=47 - i*2, y=127 - i*2, width=706 + i*4, height=266 + i*4)
            self.glow_frames.append(f)
        self.text_frame_bg.lift()

        self.text_label_shadow = tk.Label(self.text_frame, text="", fg="#557799", bg="#101025",
                                          font=self.custom_font, wraplength=680, justify="left")
        self.text_label_shadow.place(x=22, y=22)

        self.text_label = tk.Label(self.text_frame, text="", fg="#bbddff", bg="#101025",
                                   font=self.custom_font, wraplength=680, justify="left")
        self.text_label.place(x=20, y=20)

        # Buttons
        self.button_frame = tk.Frame(root, bg="#000010")
        self.button_frame.place(relx=0.5, y=420, anchor="center")

        self.button1 = self.create_interstellar_button(self.button_frame, "", 0)
        self.button2 = self.create_interstellar_button(self.button_frame, "", 1)

        self.level = 0
        self.fade_animation_id = None
        self.display_level()

        # Animate backgrounds
        self.animate_starfield()
        self.animate_nebula()

    def create_starfield(self, count):
        for _ in range(count):
            x = random.uniform(0, 800)
            y = random.uniform(0, 600)
            size = random.uniform(1, 2.5)
            speed = random.uniform(0.1, 0.4)
            star = {
                "id": self.canvas.create_oval(x, y, x + size, y + size, fill="#aaddff", outline=""),
                "x": x,
                "y": y,
                "size": size,
                "speed": speed,
                "twinkle_phase": random.uniform(0, 2 * math.pi)
            }
            self.starfield.append(star)

    def animate_starfield(self):
        for star in self.starfield:
            star["twinkle_phase"] += 0.1
            brightness = 150 + 100 * math.sin(star["twinkle_phase"])
            brightness = max(100, min(255, brightness))
            hex_bright = f"{int(brightness):02x}"
            color = f"#{hex_bright}{hex_bright}ff"
            self.canvas.itemconfig(star["id"], fill=color)
            star["x"] -= star["speed"]
            if star["x"] < 0:
                star["x"] = 800
                star["y"] = random.uniform(0, 600)
            self.canvas.coords(star["id"], star["x"], star["y"], star["x"] + star["size"], star["y"] + star["size"])
        self.root.after(50, self.animate_starfield)

    def create_nebula(self):
        colors = ["#221144", "#332266", "#443377", "#554488"]
        for _ in range(20):
            x = random.uniform(100, 700)
            y = random.uniform(100, 500)
            r = random.uniform(50, 120)
            color = random.choice(colors)
            circle = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                             fill=color, outline="", stipple="gray50")
            self.nebula_circles.append({
                "id": circle, "x": x, "y": y, "r": r,
                "dir": random.choice([-1, 1]), "phase": random.uniform(0, 2 * math.pi)
            })

    def animate_nebula(self):
        stipple_patterns = ["gray12", "gray25", "gray50", "gray75"]
        for neb in self.nebula_circles:
            neb["phase"] += 0.02 * neb["dir"]
            alpha = int((math.sin(neb["phase"]) + 1) * 1.5)
            pattern = stipple_patterns[min(alpha, len(stipple_patterns) - 1)]
            self.canvas.itemconfig(neb["id"], stipple=pattern)
        self.root.after(100, self.animate_nebula)

    def create_interstellar_button(self, parent, text, choice_index):
        btn = tk.Button(parent, text=text, width=28,
                        font=self.custom_font,
                        bg="#111122", fg="#aaddff",
                        activebackground="#224466", activeforeground="#cceeff",
                        bd=0, relief="flat", highlightthickness=3, highlightbackground="#55aaff",
                        command=lambda idx=choice_index: self.next_level(idx))
        btn.grid(row=0, column=choice_index, padx=30, pady=10)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#224466", fg="#cceeff", highlightbackground="#88bbff"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#111122", fg="#aaddff", highlightbackground="#55aaff"))
        return btn

    def fade_in_text(self, text, idx=0):
        if idx > len(text):
            return
        displayed = text[:idx]
        self.text_label_shadow.config(text=displayed)
        self.text_label.config(text=displayed)
        self.fade_animation_id = self.root.after(30, self.fade_in_text, text, idx + 1)

    def display_level(self):
        if self.fade_animation_id:
            self.root.after_cancel(self.fade_animation_id)
            self.fade_animation_id = None

        level_data = game_levels[self.level]
        story = level_data["story"]
        choices = level_data["choices"]
        self.fade_in_text(story)
        self.button1.config(text=choices[0])
        self.button2.config(text=choices[1])

    def show_reward_screen(self):
        # Clear or hide existing UI
        self.text_label.config(text="")
        self.text_label_shadow.config(text="")
        self.button_frame.place_forget()

        # Prepare reward message
        if self.moral_points >= 3:
            message = "You stayed true to your values.\nHumanity is grateful."
            color = "#aaffaa"
        elif self.moral_points >= 0:
            message = "You made difficult decisions.\nThe burden is heavy."
            color = "#ffaa55"
        else:
            message = "Power without conscience leads to ruin.\nReflect on your path."
            color = "#ff7777"

        final_label = tk.Label(self.root, text=message, fg=color, bg="#000010",
                               font=self.header_font, justify="center", wraplength=700)
        final_label.place(relx=0.5, rely=0.4, anchor="center")

        btn_frame = tk.Frame(self.root, bg="#000010")
        btn_frame.place(relx=0.5, rely=0.7, anchor="center")

        replay = tk.Button(btn_frame, text="Play Again", width=20,
                           font=self.custom_font,
                           bg="#111122", fg="#aaddff",
                           bd=0, relief="flat", highlightthickness=3, highlightbackground="#55aaff",
                           command=lambda: self.restart_game())
        replay.grid(row=0, column=0, padx=20)

        quitb = tk.Button(btn_frame, text="Quit", width=20,
                          font=self.custom_font,
                          bg="#111122", fg="#aaddff",
                          bd=0, relief="flat", highlightthickness=3, highlightbackground="#55aaff",
                          command=lambda: self.root.quit())
        quitb.grid(row=0, column=1, padx=20)

    def restart_game(self):
        # Reset game state and UI
        self.moral_points = 0
        self.level = 0
        # Place back the buttons
        self.button_frame.place(relx=0.5, y=420, anchor="center")
        # Remove reward UI labels
        for widget in self.root.place_slaves():
            # we only want to remove the final_label and the btn_frame
            # we can check if it's not part of main UI (optional)
            pass
        # Redraw the level
        self.display_level()

    def next_level(self, choice_index):
        # Assign moral points
        if choice_index == 0:
            self.moral_points += 1
        else:
            self.moral_points -= 1

        if self.level == len(game_levels) - 1:
            self.show_reward_screen()
        else:
            self.level += 1
            self.display_level()


class GameMenu:
    def __init__(self, root, start_callback):
        self.root = root
        self.start_callback = start_callback

        self.menu_frame = tk.Frame(self.root, bg="#000010")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(self.menu_frame, text="Critical.com",
                         fg="#99d9ff", bg="#000010",
                         font=("Courier New", 36, "bold"))
        title.pack(pady=(0, 50))

        play_btn = tk.Button(self.menu_frame, text="Play", width=20, height=2,
                             font=("Courier New", 16, "bold"),
                             bg="#111122", fg="#aaddff",
                             activebackground="#224466", activeforeground="#cceeff",
                             bd=0, relief="flat", highlightthickness=4, highlightbackground="#55aaff",
                             cursor="hand2",
                             command=self.on_play)
        play_btn.pack(pady=10)

        quit_btn = tk.Button(self.menu_frame, text="Quit", width=20, height=2,
                             font=("Courier New", 16, "bold"),
                             bg="#111122", fg="#aaddff",
                             activebackground="#661111", activeforeground="#ffbbbb",
                             bd=0, relief="flat", highlightthickness=4, highlightbackground="#aa5555",
                             cursor="hand2",
                             command=self.root.quit)
        quit_btn.pack(pady=10)

    def on_play(self):
        self.menu_frame.destroy()
        self.start_callback()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Critical.com")
    root.geometry("800x600")
    root.configure(bg="#000010")
    root.resizable(False, False)

    def start_game():
        game = InterstellarGame(root)

    menu = GameMenu(root, start_game)
    root.mainloop()
