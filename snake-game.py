import tkinter as tk
import random
import os

class LevelSelection:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        
        # Create the level selection window
        self.level_window = tk.Toplevel(root)
        self.level_window.title("Select Level")
        
        # Create a label and radio buttons for level selection
        tk.Label(self.level_window, text="Select Level:", font=('Arial', 16)).pack(pady=10)
        self.level_var = tk.IntVar(value=1)
        
        tk.Radiobutton(self.level_window, text="Level 1 (Normal Speed)", variable=self.level_var, value=1, font=('Arial', 14)).pack()
        tk.Radiobutton(self.level_window, text="Level 2 (Fast Speed)", variable=self.level_var, value=2, font=('Arial', 14)).pack()
        
        tk.Button(self.level_window, text="Start Game", command=self.start_game, font=('Arial', 14)).pack(pady=10)

    def start_game(self):
        level = self.level_var.get()
        self.level_window.destroy()  # Close the level selection window
        self.start_game_callback(level)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Create canvas for the game
        self.canvas = tk.Canvas(root, width=400, height=400, bg='black')
        self.canvas.pack()

        # Create a frame for the score
        self.score_frame = tk.Frame(root, bg='black')
        self.score_frame.pack(fill=tk.X, side=tk.TOP)

        # Create a label to display the score and high score
        self.score_label = tk.Label(self.score_frame, text="Score: 0  High Score: 0", bg='black', fg='white', font=('Arial', 16))
        self.score_label.pack()

        # Load high score from file
        self.load_high_score()

        # Show level selection window
        LevelSelection(root, self.start_game)

    def start_game(self, level):
        self.level = level
        self.initialize_game()
        self.root.deiconify()  # Show the main window after level selection

    def initialize_game(self):
        # Initialize game state
        self.snake = [(60, 60), (40, 60), (20, 60)]  # Start with a longer snake
        self.food = self.place_food()
        self.direction = 'Right'
        self.running = True
        self.score = 0
        self.speed = 100  # Default speed (Normal Speed)

        if self.level == 2:
            self.speed = 70  # Faster speed for Level 2

        # Setup controls and start the game loop
        self.setup_controls()
        self.update_game()

    def setup_controls(self):
        self.root.bind('<Up>', lambda event: self.change_direction('Up'))
        self.root.bind('<Down>', lambda event: self.change_direction('Down'))
        self.root.bind('<Left>', lambda event: self.change_direction('Left'))
        self.root.bind('<Right>', lambda event: self.change_direction('Right'))

    def change_direction(self, new_direction):
        if (self.direction == 'Up' and new_direction != 'Down') or \
           (self.direction == 'Down' and new_direction != 'Up') or \
           (self.direction == 'Left' and new_direction != 'Right') or \
           (self.direction == 'Right' and new_direction != 'Left'):
            self.direction = new_direction

    def place_food(self):
        while True:
            x = random.randint(1, 18) * 20
            y = random.randint(1, 18) * 20
            if (x, y) not in self.snake:
                if not (x < 20 or x >= 380 or y < 20 or y >= 380):
                    return (x, y)

    def update_game(self):
        if self.running:
            self.move_snake()
            self.check_collisions()
            self.render()
            self.update_score_label()
            self.root.after(self.speed, self.update_game)
        else:
            self.display_game_over()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            head_y -= 20
        elif self.direction == 'Down':
            head_y += 20
        elif self.direction == 'Left':
            head_x -= 20
        elif self.direction == 'Right':
            head_x += 20
        new_head = (head_x, head_y)
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self.place_food()
            self.score += 10  # Increase score
            if self.score > self.high_score:
                self.high_score = self.score
        else:
            self.snake = [new_head] + self.snake[:-1]

    def check_collisions(self):
        head = self.snake[0]
        if (head in self.snake[1:] or 
            head[0] < 20 or head[0] >= 380 or 
            head[1] < 20 or head[1] >= 380):
            self.running = False

    def render(self):
        self.canvas.delete("all")
        
        # Draw walls in light blue
        self.canvas.create_rectangle(0, 0, 400, 20, fill='lightblue')  # Top wall
        self.canvas.create_rectangle(0, 380, 400, 400, fill='lightblue')  # Bottom wall
        self.canvas.create_rectangle(0, 20, 20, 380, fill='lightblue')  # Left wall
        self.canvas.create_rectangle(380, 20, 400, 380, fill='lightblue')  # Right wall

        # Draw corner walls
        self.canvas.create_rectangle(0, 0, 20, 20, fill='lightblue')  # Top-left corner
        self.canvas.create_rectangle(380, 0, 400, 20, fill='lightblue')  # Top-right corner
        self.canvas.create_rectangle(0, 380, 20, 400, fill='lightblue')  # Bottom-left corner
        self.canvas.create_rectangle(380, 380, 400, 400, fill='lightblue')  # Bottom-right corner

        # Draw snake with more realistic segments
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                self.canvas.create_oval(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill='darkgreen')
            else:  # Body segments
                self.canvas.create_oval(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill='green')

        # Draw food as a circle
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill='red')

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}  High Score: {self.high_score}")

    def display_game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(200, 180, text=f"Game Over! Your Score: {self.score}", fill='white', font=('Arial', 16))
        self.canvas.create_text(200, 220, text=f"High Score: {self.high_score}", fill='white', font=('Arial', 16))
        self.canvas.create_text(200, 260, text="Press 'r' to Restart", fill='white', font=('Arial', 16))
        self.root.bind('<r>', self.restart_game)
        
        # Save high score to file
        self.save_high_score()

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read().strip())
        else:
            self.high_score = 0

    def restart_game(self, event):
        self.initialize_game()
        self.root.unbind('<r>')

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window until the level selection is done
    game = SnakeGame(root)
    root.mainloop()
