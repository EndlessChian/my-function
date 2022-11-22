#!usr/bin/env python
# coding=utf-8
import turtle
from random import choice

space = 2

give_color = {
    0: ('gray', '', 0, 0),
    2: ('mediumblue', 'aliceblue', 32, 38),
    4: ((0, 147, 221), 'lime', 32, 38),
    8: ('yellow', 'palevioletred', 32, 38),
    16: ('tomato', 'lightsteelblue', 32, 24),
    32: ('indigo', 'mediumslateblue', 32, 24),
    64: ('royalblue', 'paleturquoise', 32, 24),
    128: ((255, 150, 37), 'cyan', 32, 12),
    256: ('gold', 'mintcream', 32, 12),
    512: ('mediumorchid', 'cornsilk', 32, 12),
    1024: ('lavender', 'palegreen', 28, 10),
    2048: ('magenta','turquoise', 28, 10),
    4096: ('firebrick', 'plum', 28, 10),
    8192: ('darkviolet', 'chartreuse', 28, 10),
}

dary = turtle.Screen()
turtle.colormode(255)
turtle.hideturtle()
dary.setup(430, 630, 300, 50)
dary.bgcolor('gray')
dary.title('2048')
dary.tracer(0)

class Draw(turtle.Turtle):
    def __init__(self):
        super(Draw, self).__init__()
        self.penup()
        self.hideturtle()

    def draw_cube(self, x, y, num):
        x, y = (x-2)*100,10-y*100
        fc, nc, fz, pos = give_color.get(num, ('purple','crimson', 25, 5))#give_color[num]
        self.penup()
        self.goto(x+space, y+space)
        self.color('gray', fc)
        self.pendown()
        self.begin_fill()
        self.goto(x+100-space, y+space)
        self.goto(x+100-space, y+100-space)
        self.goto(x+space, y+100-space)
        self.end_fill()
        self.penup()
        if fz:
            self.goto(x+pos, y+25)
            self.color(nc)
            self.write(str(num), 'center', font=("Arial", fz, "bold"))

class Block(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()

    def grow(self):
        global block2, pit,EXIT
        if not empty:
            if fin is False: self.check()
            return
        if TIME == -1:
            EXIT = True
            draw_time()
        pit += 1
        bc_pit.show_block(pit, 'pit')
        num = choice((2, 2, 2, 2, 4))
        a, b = choice(empty)
        block2[a][b] = num
        draw.draw_cube(a, b, num)
        empty.remove((a, b))

    def go_down(self):
        if fin:return
        for i in range(4):
            while any(self.judge(i, u, i, u + 1) for u in (2, 1, 0)):pass#0.050631333692706906
        self.go()

    def go_up(self):
        if fin:return
        for i in range(4):
            while any(self.judge(i, u, i, u - 1) for u in (1, 2, 3)):pass
        self.go()

    def go_left(self):
        if fin:return
        for u in range(4):
            while any(self.judge(i, u, i - 1, u) for i in (1, 2, 3)):pass
        self.go()

    def go_right(self):
        if fin:return
        for u in range(4):
            while any(self.judge(i, u, i + 1, u) for i in (2, 1, 0)):pass
        self.go()

    def go(self):
        if pit & 10 == 10: draw.clear()
        for x in range(4):
            for y in range(4):
                draw.draw_cube(x, y, block2[x][y])
        self.grow()
    @staticmethod
    def judge(i,u,y,x):
        global block2, score, top_score
        a, b = block2[i][u], block2[y][x]
        if a == 0:return False
        elif b == 0: empty.remove((y, x))
        elif b == a:
            score += a
            bc_score.show_block(score, 'score')
            if score > top_score:
                top_score = score
                bc_top_score.show_block(top_score, 'top_score')
            if a == 1024:  win_lose.show_text("达成2048，继续请按回车键")
        else:return False
        block2[y][x] += a; block2[i][u] = 0
        empty.append((i, u))
        return True
    @staticmethod
    def check():
        for i in range(4):
            for u in range(4):
                b = block2[i][u]
                if b == 0 or u < 3 and (b == block2[i][u+1] or block2[u][i] == block2[u+1][i]):return
        global fin; fin = True
        win_lose.show_text('游戏结束，重新开始请按空格键')

class Background(turtle.Turtle):
    __position = {
        'pit': ('gold', space-200, 210, '步数：', (-115, 210)),
        'time': ('mistyrose', space-200, 125, '用时：', (-115, 135)),
        'score': ('yellow', 15, 210, '得分：', (105, 210)),
        'top_score': ('orange', 15, 125, '最高得分', (105, 135)),
    }

    def __init__(self):
        super(Background, self).__init__()
        self.penup(); self.hideturtle()

    def show_block(self, msg, pos):
        cor, x, y, til, ipos = self.__position[pos]
        self.goto(x, y); self.color('white', cor)
        self.clear()
        self.pendown(); self.begin_fill()
        self.goto(x+185-space, y); self.goto(x+185-space, y+80); self.goto(x, y+80)
        self.end_fill(); self.penup()
        self.goto(x+90, y+50); self.color('blue', 'bisque')
        self.write(f'{til}', align='center', font=("Arial", 18, "bold"))
        self.color('white'); self.goto(ipos)
        self.write(f'{msg}', align='center', font=("Arial", 20, "bold"))

class WinLose(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup(); self.ht(); self.color('red')
    def show_text(self, text): self.write(f'{text}', align='center', font=("黑体", 20, "bold"))

def init():
    global score, empty, block, block2, fin, pit, TIME
    score, pit = 0, -1
    if fin:
        TIME, fin = -1, False
    else:TIME = 0
    block2 = [[0]*4 for i in range(4)]
    empty = [(i, u) for i in range(4) for u in range(4)]
    win_lose.clear()
    block = Block()
    bc_score.show_block(0, 'score')
    block.go()

def draw_time():
    global TIME
    if fin:return
    TIME += 1
    bc_time.show_block(TIME, 'time')
    dary.ontimer(draw_time, 995)

fin, EXIT = False, False
score, top_score, pit, TIME = 0, 0, -1, -1
empty = [(i, u) for i in range(4) for u in range(4)]
block2 = [[0]*4 for i in range(4)]
draw = Draw()
bc_pit = Background()
bc_time = Background()
bc_score = Background()
bc_top_score = Background()
bc_time.show_block(0, 'time')
bc_score.show_block(0, 'score')
bc_top_score.show_block(0, 'top_score')
block = Block()
block.grow()
move_time = 0.1
win_lose = WinLose()
dary.listen()
dary.onkey(block.go_right, 'Right')
dary.onkey(block.go_left, 'Left')
dary.onkey(block.go_up, 'Up')
dary.onkey(block.go_down, 'Down')
dary.onkey(win_lose.clear, 'Return')
dary.onkey(init, 'space')
dary.onkey(lambda : dary.bye(), 'Escape')
if __name__ == '__main__':
    while not EXIT:  dary.update()
    dary.mainloop()
