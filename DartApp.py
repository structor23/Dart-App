import tkinter as tk
from tkinter import messagebox
import random
import time

class DartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dart 501 Spiel")
        self.player_score = 501
        self.bot_score = 501
        self.rounds_played = 0  # Track the number of rounds played
        self.player_total_points = 0  # Total points scored by player
        self.bot_total_points = 0  # Total points scored by bot
        self.is_player_turn = True

        # Frame for Scores
        score_frame = tk.Frame(root)
        score_frame.pack(pady=20)

        self.player_label = tk.Label(score_frame, text="Spieler", font=("Arial", 18))
        self.player_label.grid(row=0, column=0, padx=20)

        self.bot_label = tk.Label(score_frame, text="Gegner", font=("Arial", 18))
        self.bot_label.grid(row=0, column=1, padx=20)

        self.player_score_label = tk.Label(score_frame, text="501", font=("Arial", 24))
        self.player_score_label.grid(row=1, column=0, padx=20)

        self.bot_score_label = tk.Label(score_frame, text="501", font=("Arial", 24))
        self.bot_score_label.grid(row=1, column=1, padx=20)

        self.player_average_label = tk.Label(score_frame, text="0.0", font=("Arial", 10))
        self.player_average_label.grid(row=2, column=0, padx=20)

        self.bot_average_label = tk.Label(score_frame, text="0.0", font=("Arial", 10))
        self.bot_average_label.grid(row=2, column=1, padx=20)

        self.entry = tk.Entry(root, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda event: self.update_score())  # Bind Enter key

        self.button = tk.Button(root, text="Punkte eingeben", font=("Arial", 18), command=self.update_score)
        self.button.pack(pady=10)

        self.bot_hits_label = tk.Label(root, text="Gegner wirft: ", font=("Arial", 18))
        self.bot_hits_label.pack(pady=10)

        self.bot_round_points_label = tk.Label(root, text="Gesamtwurf Gegner: 0", font=("Arial", 18))
        self.bot_round_points_label.pack(pady=10)
        
        self.rounds_label = tk.Label(root, text="Runde: 0", font=("Arial", 18))  # Display rounds played
        self.rounds_label.pack(pady=10)

    def update_score(self):
        if self.is_player_turn:
            self.player_turn()
        else:
            self.root.after(1000, self.bot_turn)  # Delay bot's turn by 1 second

    def player_turn(self):
        try:
            points = int(self.entry.get())
            if points < 0 or points > 180:
                raise ValueError("Ungültige Punktzahl")
            self.player_total_points += points
            self.player_score -= points
            if self.player_score < 0:
                messagebox.showinfo("Spielstand", "Überworfen! Punktzahl bleibt unverändert.")
                self.player_score += points
                self.player_total_points -= points
            elif self.player_score == 0:
                messagebox.showinfo("Spielstand", "Du hast gewonnen!")
                self.reset_game()
            self.player_score_label.config(text=f"{self.player_score}")
            self.entry.delete(0, tk.END)
            self.is_player_turn = False
            self.update_score()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Punktzahl ein.")
            self.entry.delete(0, tk.END)

    def bot_turn(self):
        hits = []  # List to store hits
        round_points = 0  # Points scored in the current round
        for dart in range(3):  # Simulate 3 darts per round
            if self.bot_score > 40 or self.bot_score == 40:  # If bot score is greater than 40 or exactly 40
                if dart < 2:  # First two darts aim for Triple 20
                    points, throw = self.simulate_bot_throw(aim="triple20")
                else:  # Third dart aims for Triple 19 if previous misses
                    points, throw = self.simulate_bot_throw(aim="triple19")
            else:
                points, throw = self.bot_checkout(self.bot_score)  # Aim for checkout

            # Skip invalid checkouts
            if throw == "Invalid Checkout":
                continue

            hits.append(throw)
            round_points += points
            self.bot_total_points += points
            self.bot_score -= points
            self.bot_hits_label.config(text=f"Gegner wirft: {', '.join(hits)}")
            self.root.update()
            time.sleep(0.5)  # Half the original delay
            if self.bot_score == 0:
                messagebox.showinfo("Spielstand", f"Der Gegner hat mit {throw} ausgecheckt!")
                self.bot_score_label.config(text=f"{self.bot_score}")
                self.bot_hits_label.config(text=f"Gegner wirft: {', '.join(hits)}")
                self.reset_game()
                return
            elif self.bot_score < 0:
                self.bot_score += points  # Bot cannot checkout
                self.bot_total_points -= points
                break
        self.rounds_played += 1  # Increment rounds played
        self.bot_round_points_label.config(text=f"Gesamtwurf Gegner: {round_points}")  # Update round points display     
        self.rounds_label.config(text=f"Runde: {self.rounds_played}")  # Update rounds display
        self.bot_score_label.config(text=f"{self.bot_score}")
        self.bot_hits_label.config(text=f"Gegner wirft: {', '.join(hits)}")
        self.update_average()
        self.animate_total_score()  # Animate total score
        self.is_player_turn = True

    def bot_checkout(self, score):
        checkouts = {
            170: "T20, T20, Bullseye", 167: "T20, T19, Bullseye", 164: "T20, T18, Bullseye",
            161: "T20, T17, Bullseye", 160: "T20, T20, D20", 158: "T20, T20, D19",
            157: "T20, T19, D20", 156: "T20, T20, D18", 155: "T20, T19, D19", 
            154: "T20, T18, D20", 153: "T20, T19, D18", 152: "T20, T20, D16", 
            151: "T20, T17, D20", 150: "T20, T18, D18", 149: "T20, T19, D16", 
            148: "T20, T16, D20", 147: "T20, T17, D18", 146: "T20, T18, D16", 
            145: "T20, T15, D20", 144: "T20, T20, D12", 143: "T20, T17, D16", 
            142: "T20, T14, D20", 141: "T20, T19, D12", 140: "T20, T16, D16", 
            139: "T20, T13, D20", 138: "T20, T18, D12", 137: "T20, T15, D16", 
            136: "T20, T20, D8", 135: "T20, T17, D12", 134: "T20, T14, D16", 
            133: "T20, T19, D8", 132: "T20, T16, D12", 131: "T20, T13, D16", 
            130: "T20, T18, D8", 129: "T19, T16, D12", 128: "T18, T14, D16", 
            127: "T20, T17, D8", 126: "T19, T19, D6", 125: "T18, T13, D16", 
            124: "T20, T16, D8", 123: "T19, T16, D9", 122: "T18, T18, D7", 
            121: "T20, T15, D8", 120: "T20, S20, D20", 119: "T20, S19, D20", 
            118: "T20, S18, D20", 117: "T20, S17, D20", 116: "T20, S16, D20", 
            115: "T20, S15, D20", 114: "T20, S14, D20", 113: "T20, S13, D20", 
            112: "T20, S12, D20", 111: "T20, S11, D20", 110: "T20, S10, D20", 
            109: "T20, S9, D20", 108: "T20, S8, D20", 107: "T20, S7, D20", 
            106: "T20, S6, D20", 105: "T20, S5, D20", 104: "T18, S18, D16", 
            103: "T17, S12, D20", 102: "T20, S10, D16", 101: "T17, S14, D20", 
            100: "T20, D20", 99: "T19, S10, D16", 98: "T20, D19", 
            97: "T19, D20", 96: "T20, D18", 95: "T19, D19", 
            94: "T18, D20", 93: "T19, D18", 92: "T20, D16", 
            91: "T17, D20", 90: "T18, D18", 89: "T19, D16", 
            88: "T20, D14", 87: "T17, D18", 86: "T18, D16", 
            85: "T15, D20", 84: "T20, D12", 83: "T17, D16", 
            82: "Bullseye, D16", 81: "T19, D12", 80: "T20, D10", 
            79: "T19, D11", 78: "T18, D12", 77: "T19, D10", 
            76: "T20, D8", 75: "T17, D12", 74: "T14, D16", 
            73: "T19, D8", 72: "T16, D12", 71: "T13, D16", 
            70: "T18, D8", 69: "T19, D6", 68: "T20, D4", 
            67: "T17, D8", 66: "T10, D18", 65: "T19, D4", 
            64: "T16, D8", 63: "T13, D12", 62: "T10, D16", 
            61: "T15, D8", 60: "S20, D20", 59: "S19, D20", 
            58: "S18, D20", 57: "S17, D20", 56: "S16, D20", 
            55: "S15, D20", 54: "S14, D20", 53: "S13, D20", 
            52: "S12, D20", 51: "S11, D20", 50: "Bullseye", 
            49: "S17, D16", 48: "S16, D16", 47: "S15, D16", 
            46: "S14, D16", 45: "S13, D16", 44: "S12, D16", 
            43: "S11, D16", 42: "S10, D16", 41: "S9, D16", 
            40: "D20", 38: "D19", 36: "D18", 
            34: "D17", 32: "D16", 30: "D15", 
            28: "D14", 26: "D13", 24: "D12", 
            22: "D11", 20: "D10", 18: "D9", 
            16: "D8", 14: "D7", 12: "D6", 
            10: "D5", 8: "D4", 6: "D3", 
            4: "D2", 2: "D1"
        }
        if score in checkouts:
            return score, checkouts[score]
        else:
            return score, "Invalid Checkout"

    def simulate_bot_throw(self, aim):
        # Realistic simulation of a PDC player's throw
        if aim == "triple20":
            probabilities = {
                60: 0.50,  # 50% chance to hit 60 (triple 20)
                20: 0.20,  # 20% chance to hit 20 (single 20)
                5: 0.10,   # 10% chance to hit 5
                1: 0.10,   # 10% chance to hit 1
                15: 0.05,  # 5% chance to hit 15 (triple 5)
                3: 0.05    # 5% chance to hit 3 (triple 1)
            }
            throws = {60: "T20", 20: "20", 5: "5", 1: "1", 15: "T5", 3: "T1"}
        elif aim == "triple19":
            probabilities = {
                57: 0.50,  # 50% chance to hit 57 (triple 19)
                19: 0.20,  # 20% chance to hit 19 (single 19)
                3: 0.10,   # 10% chance to hit 3
                7: 0.10,   # 10% chance to hit 7
                21: 0.05,  # 5% chance to hit 21 (triple 7)
                9: 0.05    # 5% chance to hit 9 (triple 3)
            }
            throws = {57: "T19", 19: "19", 3: "3", 7: "7", 21: "T7", 9: "T3"}
        scores = list(probabilities.keys())
        chances = list(probabilities.values())
        points = random.choices(scores, chances)[0]
        return points, throws[points]

    def update_average(self):
        if self.rounds_played > 0:
            player_average = self.player_total_points / self.rounds_played
            bot_average = self.bot_total_points / self.rounds_played
            self.player_average_label.config(text=f"{player_average:.2f}")
            self.bot_average_label.config(text=f"{bot_average:.2f}")

    def animate_total_score(self):
        # Simple animation to highlight the total score update
        for i in range(3):
            self.bot_score_label.config(fg='red')
            self.root.update()
            time.sleep(0.1)  # Half the original delay
            self.bot_score_label.config(fg='black')
            self.root.update()
            time.sleep(0.1)  # Half the original delay

    def reset_game(self):
        self.player_score = 501
        self.bot_score = 501
        self.rounds_played = 0  # Reset rounds played
        self.player_total_points = 0  # Reset total points for player
        self.bot_total_points = 0  # Reset total points for bot
        self.player_score_label.config(text="501")
        self.bot_score_label.config(text="501")
        self.bot_hits_label.config(text="Gegner wirft: ")  # Reset hits display
        self.bot_round_points_label.config(text="Gesamtwurf Gegner: 0")  # Reset round points display
        self.rounds_label.config(text="Runde: 0")  # Reset rounds display
        self.player_average_label.config(text="0.0")  # Reset player average display
        self.bot_average_label.config(text="0.0")  # Reset bot average display
        self.is_player_turn = True

if __name__ == "__main__":
    root = tk.Tk()
    app = DartApp(root)
    root.mainloop()
