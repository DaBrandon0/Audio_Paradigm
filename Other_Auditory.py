import tkinter as tk
import random 
import os
from playsound import playsound

ROUNDS = 10

def play_audio(voice, word):
    # Play the audio file
    file_name = f"{voice}_{word}.mp3"
    base_path = os.path.join(os.path.dirname(__file__), "Voices")
    file_path = os.path.join("Voices", file_name)
    playsound(file_path)

class Auditory:
    def __init__(self, root):
        self.root = root
        self.root.title("Auditory Paradigm")
        self.voices = ["Man", "Woman", "Child", "Robot"]
        self.rand_voice = random.choice(self.voices)
        self.rand_word = random.choice(self.voices)

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window dimensions
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Initialize score and game state
        self.score = 0
        self.countdown = 3
        self.x = 0
        self.y = 0
        self.accept_input = False  
        self.accept_restart = False
        self.accept_start = False
        self.round_number = 0

        # Set up the Text widget for message display
        self.message_label = tk.Text(
            root, 
            height=5, 
            width=20, 
            font=("Arial", 100), 
            wrap="word", 
            bg="#F0F0F0", 
            relief="flat", 
            bd=0
        )
        self.message_label.tag_configure("center", justify="center")
        self.message_label.place(relx=0.5, rely=0.7, anchor="center")

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.place(relx=0.5, rely=0.90, anchor="center")

        # Key event listeners
        self.root.bind("<KeyPress-y>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-n>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-r>", lambda event: self.restart_game(True))
        self.root.bind("<KeyPress-space>", lambda event: self.start_game(True))

        # listen to asdf 
        self.root.bind("<KeyPress-a>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-s>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-d>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-f>", lambda event: self.process_input(True))

        # listen to jkl;
        self.root.bind("<KeyPress-j>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-k>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-l>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-semicolon>", lambda event: self.process_input(False))

        self.start_screen()
    
    def start_screen(self):
        self.message_label.config(state="normal")
        self.message_label.delete("1.0", "end")
        self.message_label.insert("end", "Press SPACE to start", "center")
        self.message_label.config(state="disabled")
        self.accept_start = True
    
    def count(self):
        if self.countdown > 0:
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, str(self.countdown), "center")
            self.message_label.configure(state="disabled")
            self.countdown -= 1
            self.root.after(1000, self.count)
        else:
            self.start_round()
    
    def start_round(self):
        if self.round_number < ROUNDS:
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, f"Listen", "center")
            self.message_label.configure(state="disabled")
            self.root.after(100, self.promt)
        else:
            self.show_final()
    def promt(self):
        rand = random.randint(1, 100)
        self.rand_voice = random.choice(self.voices)
        self.rand_word = self.rand_voice
        #Play correct word
        if rand <= 25:
            while(self.rand_voice == self.rand_word):
                self.rand_word = random.choice(self.voices)

            play_audio(self.rand_voice, self.rand_word)
        else: 
            self.countdown = 0
            play_audio(self.rand_voice, self.rand_word)

        self.message_label.config(state="normal")
        self.message_label.delete("1.0", "end")
        self.message_label.insert("end", "Matched?", "center")
        self.message_label.config(state="disabled")

        self.accept_input = True
        self.root.after(2000, self.show_blank)

    def show_blank(self):
        self.accept_input = False
        self.round_number += 1
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.configure(state="disabled")

        #CHANGE THIS TO CHANGE THE BLANK TIME BETWEEN THE ROUNDS
        possible_delay = [750, 1000, 1250]
        random_delay = random.choice(possible_delay)
        self.root.after(random_delay, self.start_round)
    
    def show_final(self):
        # Display final score
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, f"Final Score: {self.score}\n Press R to Restart", "center")
        self.message_label.configure(state="disabled")
        self.accept_restart = True   
    
    def process_input(self, user_said_yes):
        # Process yes or no
        if not self.accept_input:
            return

        self.accept_input = False

        if (user_said_yes and self.rand_voice == self.rand_word) or (not user_said_yes and self.rand_voice != self.rand_word):
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}")
    
    def restart_game(self, restart):
        # Restart the game
        if not self.accept_restart:
            return
        self.accept_restart = False
        self.round_number = 0
        self.countdown = 3
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.start_screen() 

    def start_game(self, start):
        # Start the game
        if not self.accept_start:
            return
        self.accept_start = False
        self.round_number = 0
        self.countdown = 3
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.count()
            

if __name__ == "__main__":
    root = tk.Tk()
    app = Auditory(root)
    root.mainloop()