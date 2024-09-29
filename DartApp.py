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

        self.rounds_label = tk.Label(root, text="Gespielte Runden: 0", font=("Arial", 18))  # Display rounds played
        self.rounds_label.pack(pady=10)

        self.bot_round_points_label = tk.Label(root, text="Gegner Punkte diese Runde: 0", font=("Arial", 18))
        self.bot_round_points_label.pack(pady=10)

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

            hits.append(throw)
            round_points += points
            self.bot_total_points += points
            self.bot_score -= points
            self.bot_hits_label.config(text=f"Gegner wirft: {throw}")  # Update hits display with delay
            self.root.update()  # Update the GUI
            time.sleep(1)  # Delay for 1 second to simulate real throw
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
        self.rounds_label.config(text=f"Gespielte Runden: {self.rounds_played}")  # Update rounds display
        self.bot_score_label.config(text=f"{self.bot_score}")
        self.bot_hits_label.config(text=f"Gegner wirft: {', '.join(hits)}")  # Update hits display
        self.bot_round_points_label.config(text=f"Gegner Punkte diese Runde: {round_points}")  # Update round points display
        self.update_average()
        self.animate_total_score()  # Animate total score
        self.is_player_turn = True

    def bot_checkout(self, score):
        # Logic for bot to checkout based on current score
        if score == 40:
            return 40, "D20"  # Double 20
        elif score == 38:
            return 38, "D19"  # Double 19
        elif score == 32:
            return 32, "D16"  # Double 16
        elif score == 24:
            return 24, "D12"  # Double 12
        elif score == 16:
            return 16, "D8"  # Double 8
        elif score == 8:
            return 8, "D4"   # Double 4
        elif score == 4:
            return 4, "D2"   # Double 2
        elif score == 2:
            return 2, "D1"   # Double 1
        else:
            # If not a direct checkout, aim for single points to leave a double
            if score > 20:
                remaining = score - 20
                if remaining % 2 == 0:  # Ensure the remaining score is a double out
                    return 20, "20"
                else:
                    return score - 19, "19"  # Adjust to leave a double out
            return score, f"{score}"

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
            time.sleep(0.2)
            self.bot_score_label.config(fg='black')
            self.root.update()
            time.sleep(0.2)

    def reset_game(self):
        self.player_score = 501
        self.bot_score = 501
        self.rounds_played = 0  # Reset rounds played
        self.player_total_points = 0  # Reset total points for player
        self.bot_total_points = 0  # Reset total points for bot
        self.player_score_label.config(text="501")
        self.bot_score_label.config(text="501")
        self.bot_hits_label.config(text="Gegner wirft: ")  # Reset hits display
        self.rounds_label.config(text="Gespielte Runden: 0")  # Reset rounds display
        self.bot_round_points_label.config(text="Gegner Punkte diese Runde: 0")  # Reset round points display
        self.player_average_label.config(text="0.0")  # Reset player average display
        self.bot_average_label.config(text="0.0")  # Reset bot average display
        self.is_player_turn = True

if __name__ == "__main__":
    root = tk.Tk()
    app = DartApp(root)
    root.mainloop()