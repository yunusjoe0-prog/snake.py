import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

GRID_SIZE = 20

class SnakeGameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.food = (10, 10)
        self.score = 0
        self.game_over = False
        Clock.schedule_interval(self.update, 1.0 / 7.0)

    def spawn_food(self):
        cols = int(self.width / GRID_SIZE) or 15
        rows = int(self.height / GRID_SIZE) or 15
        while True:
            fx = random.randint(0, cols - 1)
            fy = random.randint(0, rows - 1)
            if (fx, fy) not in self.snake:
                self.food = (fx, fy)
                break

    def update(self, dt):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        cols = int(self.width / GRID_SIZE) or 15
        rows = int(self.height / GRID_SIZE) or 15

        # التصادم مع الجدران أو مع جسم الثعبان
        if (new_head[0] < 0 or new_head[0] >= cols or
            new_head[1] < 0 or new_head[1] >= rows or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # رسم الطعام (أحمر)
            Color(1, 0.2, 0.2, 1)
            Rectangle(pos=(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE),
                      size=(GRID_SIZE - 1, GRID_SIZE - 1))

            # رسم الثعبان (أخضر)
            Color(0.2, 0.9, 0.3, 1)
            for part in self.snake:
                Rectangle(pos=(part[0] * GRID_SIZE, part[1] * GRID_SIZE),
                          size=(GRID_SIZE - 1, GRID_SIZE - 1))

    def change_dir(self, new_dir):
        # منع العكس المباشر للاتجاه
        if (new_dir[0] == -self.direction[0] and new_dir[1] == 0) or \
           (new_dir[1] == -self.direction[1] and new_dir[0] == 0):
            return
        self.direction = new_dir

    def restart(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.game_over = False
        self.score = 0
        self.spawn_food()

class SnakeApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        
        self.game = SnakeGameWidget()
        main_layout.add_widget(self.game)

        # لوحة أزرار التحكم باللمس
        controls = BoxLayout(size_hint_y=0.35, orientation='vertical')
        
        row1 = BoxLayout()
        btn_up = Button(text='UP', on_press=lambda x: self.game.change_dir((0, 1)))
        row1.add_widget(Widget())
        row1.add_widget(btn_up)
        row1.add_widget(Widget())

        row2 = BoxLayout()
        btn_left = Button(text='LEFT', on_press=lambda x: self.game.change_dir((-1, 0)))
        btn_restart = Button(text='RESET', on_press=lambda x: self.game.restart())
        btn_right = Button(text='RIGHT', on_press=lambda x: self.game.change_dir((1, 0)))
        row2.add_widget(btn_left)
        row2.add_widget(btn_restart)
        row2.add_widget(btn_right)

        row3 = BoxLayout()
        btn_down = Button(text='DOWN', on_press=lambda x: self.game.change_dir((0, -1)))
        row3.add_widget(Widget())
        row3.add_widget(btn_down)
        row3.add_widget(Widget())

        controls.add_widget(row1)
        controls.add_widget(row2)
        controls.add_widget(row3)

        main_layout.add_widget(controls)
        return main_layout

if __name__ == '__main__':
    SnakeApp().run()

