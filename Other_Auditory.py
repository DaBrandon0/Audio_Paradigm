import tkinter as tk
import random 
import os
from playsound import playsound
import threading

import socket
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_stream, local_clock
import threading

"""
 
7000 + block number: Marks the start of a new block.
8000 + block number: Marks the end of the current block.

5000 + round number: Marks the start of a new round within a block.

3001: Stimulus is a match (text and color are the same).
3002: Stimulus is a mismatch (text and color are different).

4001: User correctly identified a match.
4002: User correctly identified a mismatch.

5001: User incorrectly identified a match as a mismatch.
5002: User incorrectly identified a mismatch as a match.
"""

# Setup UDP
udp_marker = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip = '127.0.0.1'
port = 12345

# Set up LSL stream
info = StreamInfo('NBackMarkers', 'Markers', 1, 0, 'string', 'visual_nback_task_001')
outlet = StreamOutlet(info)

BLOCKS = 13


class Auditory:
    # Function to send a UDP message dynamically
    def play_audio(self, voice, word):
        """ Play the audio file asynchronously in a new thread """
        def play():
            file_name = f"{voice}_{word}.mp3"
            base_path = os.path.join(os.path.dirname(__file__), "Voices")  # Absolute path
            file_path = os.path.abspath(os.path.join(base_path, file_name))  # Ensure correct format

            # Send marker
            self.sendTiD("3001" if voice == word else "3002")

            try:
                playsound(file_path)
            except Exception as e:
                print(f"Error playing sound: {e}")  # Debugging output

        audio_thread = threading.Thread(target=play)
        audio_thread.start()


    def sendTiD(self, base_message):
        message = f"{base_message} - Block {self.Block}, Round {self.round_number}"
        message = base_message
        udp_marker.sendto(message.encode('utf-8'), (ip, port))
        print(f"Sent UDP message: {message}")

    def __init__(self, root):
        self.root = root
        self.ROUNDS = 30
        self.Block = 0
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
        if self.Block < BLOCKS:
            self.sendTiD("7000")  # Event ID for block start
            self.ROUNDS = 30
            self.message_label.config(state="normal")
            self.message_label.delete("1.0", "end")
            self.message_label.insert("end", "Press SPACE to start", "center")
            self.message_label.config(state="disabled")
            self.accept_start = True
        else:
            self.root.destroy()
    
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
        if self.round_number < self.ROUNDS:
            self.sendTiD("6000")  # Event ID for round start
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, f"Listen", "center")
            self.message_label.configure(state="disabled")
            rand = random.randint(1, 100)
            self.rand_voice = random.choice(self.voices)
            self.rand_word = self.rand_voice
            #Play correct word
            if rand <= 25:
                while(self.rand_voice == self.rand_word):
                    self.rand_word = random.choice(self.voices)
                self.play_audio(self.rand_voice, self.rand_word)
            else: 
                self.countdown = 0
                self.play_audio(self.rand_voice, self.rand_word)
            self.root.after(1500, self.promt)
        else:
            self.show_final()

    def promt(self):
        self.message_label.config(state="normal")
        self.message_label.delete("1.0", "end")
        self.message_label.insert("end", "Matched?", "center")
        self.message_label.config(state="disabled")
        #self.sendTiD("PromptDisplayed")  # Event ID for prompt display
        self.accept_input = True

    def show_blank(self):
        if(self.accept_input):
            self.ROUNDS += 1
        self.accept_input = False
        self.round_number += 1
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.configure(state="disabled")

        #CHANGE THIS TO CHANGE THE BLANK TIME BETWEEN THE ROUNDS
        possible_delay = [500, 750, 1000]
        random_delay = random.choice(possible_delay)
        self.root.after(500, self.start_round)
    
    def show_final(self):
        # Display final score
        self.sendTiD("8000")  # Event ID for block end
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, f"Final Score: {self.score}\n Press R to Restart", "center")
        self.message_label.configure(state="disabled")
        self.Block += 1
        self.accept_restart = True   
    
    def process_input(self, user_said_yes):
        # Process yes or no
        if not self.accept_input:
            return

        self.accept_input = False

        correct = (user_said_yes and self.rand_voice == self.rand_word) or (not user_said_yes and self.rand_voice != self.rand_word)
        
        if correct:
            if self.rand_voice == self.rand_word:
                self.sendTiD("4001")  # Correct with Match
            else:
                self.sendTiD("4002")  # Correct with Mismatch
        else:
            if self.rand_voice == self.rand_word:
                self.sendTiD("5001")  # Incorrect with Match
            else:
                self.sendTiD("5002")  # Incorrect with Mismatch

        if correct:
            self.score += 1

        #self.score_label.config(text=f"Score: {self.score}")
        self.score_label.config(text=f"Score: {self.score}")
        self.root.after(50, self.show_blank)
    
    def restart_game(self, restart):
        # Restart the game
        if not self.accept_restart:
            return
        self.accept_restart = False
        self.round_number = 0
        self.countdown = 3
        self.score = 0
        #self.score_label.config(text=f"Score: {self.score}")
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
        #self.score_label.config(text=f"Score: {self.score}")
        self.score_label.config(text=f"Score: {self.score}")
        self.count()
            

if __name__ == "__main__":
    root = tk.Tk()
    app = Auditory(root)
    root.mainloop()