from random import randint
import tkinter as tk
from snake.tile import Tile


class SnakeGame:
    def __init__(self, cols, rows):
        self.COLS = cols
        self.ROWS = rows
        self.TILE_SIZE = 25
        self.WINDOWS_WIDTH = self.TILE_SIZE * self.ROWS
        self.WINDOWS_HEIGHT = self.TILE_SIZE * self.COLS
        self.window = tk.Tk()
        self.window.title("Snake")
        self.window.resizable(False, False)
        self.food = Tile(10 * self.TILE_SIZE, 10 * self.TILE_SIZE)
        self.snake = Tile(5 * self.TILE_SIZE, 5 * self.TILE_SIZE)
        self.snake_body = []
        self.velocityX = 0
        self.velocityY = 0
        self.game_over = False
        self.score = 0

    def center_window(self):
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_x = int((screen_width - window_width) / 2)
        window_y = int((screen_height - window_height) / 2)
        self.window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    def draw_canvas(self):
        self.canvas = tk.Canvas(
            self.window,
            width=self.WINDOWS_WIDTH,
            height=self.WINDOWS_HEIGHT,
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas.pack()

    def change_direction(self, event):
        if self.game_over:
            return
        if event.keysym == "Up" and self.velocityY != 1:
            self.velocityX = 0
            self.velocityY = -1
        elif event.keysym == "Down" and self.velocityY != -1:
            self.velocityX = 0
            self.velocityY = 1
        elif event.keysym == "Left" and self.velocityX != 1:
            self.velocityX = -1
            self.velocityY = 0
        elif event.keysym == "Right" and self.velocityX != -1:
            self.velocityX = 1
            self.velocityY = 0

    def move_snake(self):
        if self.game_over:
            return
        if (
            self.snake.x < 0
            or self.snake.x >= self.WINDOWS_WIDTH
            or self.snake.y < 0
            or self.snake.y >= self.WINDOWS_HEIGHT
        ):
            self.game_over = True
            return
        for tile in self.snake_body:
            if self.snake.x == tile.x and self.snake.y == tile.y:
                self.game_over = True
                return
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.snake_body.append(Tile(self.food.x, self.food.y))
            self.food.x = randint(0, self.COLS - 1) * self.TILE_SIZE
            self.food.y = randint(0, self.ROWS - 1) * self.TILE_SIZE
            self.score += 1
        for i in range(len(self.snake_body) - 1, -1, -1):
            self.tile = self.snake_body[i]
            if i == 0:
                self.tile.x = self.snake.x
                self.tile.y = self.snake.y
            else:
                previous_tile = self.snake_body[i - 1]
                self.tile.x = previous_tile.x
                self.tile.y = previous_tile.y
        self.snake.x += self.velocityX * self.TILE_SIZE
        self.snake.y += self.velocityY * self.TILE_SIZE

    def draw_elements(self):
        self.move_snake()
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            self.food.x,
            self.food.y,
            self.food.x + self.TILE_SIZE,
            self.food.y + self.TILE_SIZE,
            fill="red",
        )
        self.canvas.create_rectangle(
            self.snake.x,
            self.snake.y,
            self.snake.x + self.TILE_SIZE,
            self.snake.y + self.TILE_SIZE,
            fill="lime green",
        )
        for tile in self.snake_body:
            self.canvas.create_rectangle(
                tile.x,
                tile.y,
                tile.x + self.TILE_SIZE,
                tile.y + self.TILE_SIZE,
                fill="lime green",
            )
        if self.game_over:
            self.canvas.create_text(
                self.WINDOWS_WIDTH / 2,
                self.WINDOWS_HEIGHT / 2,
                text=f"Game Over! Score: {self.score}",
                fill="black",
                font=("Arial", 24),
            )
        else:
            self.canvas.create_text(
                self.WINDOWS_WIDTH - 50,
                10,
                text=f"Score: {self.score}",
                fill="black",
                font=("Arial", 16),
            )
        self.window.after(100, self.draw_elements)

    def run_game(self):
        self.draw_canvas()
        self.draw_elements()
        self.window.bind("<KeyRelease>", self.change_direction)
        self.window.update_idletasks()
        self.center_window()
        self.window.update()
        self.window.mainloop()
