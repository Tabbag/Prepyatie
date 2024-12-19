import tkinter as tk
import random

# Настройки игры
WIDTH = 400
HEIGHT = 400
PLAYER_SIZE = 20
OBSTACLE_SIZE = 20
OBSTACLE_SPEED = 5


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Избегай препятствий")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(190, 350, 190 + PLAYER_SIZE, 350 + PLAYER_SIZE, fill="yellow")
        self.obstacles = []
        self.score = 0

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.spawn_obstacle()
        self.update()

    def move_left(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x1 > 0:
            self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x2 < WIDTH:
            self.canvas.move(self.player, 20, 0)

    def spawn_obstacle(self):
        x = random.randint(0, WIDTH - OBSTACLE_SIZE)
        obstacle = self.canvas.create_rectangle(x, 0, x + OBSTACLE_SIZE, OBSTACLE_SIZE, fill="red")
        self.obstacles.append(obstacle)

    def update(self):
        for obstacle in list(self.obstacles):
            # Двигаем препятствие вниз
            self.canvas.move(obstacle, 0, OBSTACLE_SPEED)
            # Проверяем если препятствие вышло за пределы окна
            if self.canvas.coords(obstacle)[1] > HEIGHT:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1

            # Проверка на столкновение с игроком
            if not self.check_collision(obstacle):
                continue  # Если нет столкновения - продолжаем проверять другие препятствия

            # Если произошло столкновение
            print("Игра окончена! Ваш счёт:", self.score)
            self.root.destroy()
            return

        # Спавним новые препятствия
        if random.random() < 0.02:  # Вероятность появления нового препятствия
            self.spawn_obstacle()

        # Обновляем экран
        self.root.after(50, self.update)

    def check_collision(self, obstacle):
        player_coords = self.canvas.coords(self.player)

        # Проверяем координаты каждого препятствия перед обращением к ним
        if obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            return (player_coords[2] > obstacle_coords[0] and player_coords[0] < obstacle_coords[2] and
                    player_coords[3] > obstacle_coords[1] and player_coords[1] < obstacle_coords[3])

        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
