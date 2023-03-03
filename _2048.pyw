#!python3
#encoding=gbk
from os import path
import turtle
from random import choice
rpath = r'./images'
boundary = turtle.Screen()
bg = f'{rpath}\\bg.gif'
boundary.register_shape(bg) if path.exists(bg) else exit(f"This program is need {bg} .")
ii = 1
while ii < 5000:
    ii *= 2
    n = f'{rpath}\\{ii}.gif'
    boundary.register_shape(n) if path.exists(n) else exit(f"This program is need {n} .")
del n, ii, path
boundary.setup(430, 630, 400, 50)
boundary.bgcolor('gray')
boundary.title('2048')
boundary.tracer(0)

class Block(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup(); self.goto(0, 0)
        self.shape(bg); self.stamp()
        self.grow()
    def grow(self):
        global TIME, pit
        bc_time.show_msg('time', TIME)
        bc_score.show_msg('score', score)
        bc_top_score.show_msg('top_score', top_score)
        if not allpos:
            bc_pit.show_msg('pit', pit)
            if not fin:self.__check()
            return
        pit += 1
        bc_pit.show_msg('pit', pit)
        if TIME == -1: draw_time()
        num = choice((2, 2, 2, 2, 4))
        self.shape(f'{rpath}\\{num}.gif')
        a = choice(allpos)
        block2[a[0]][a[1]] = num
        self.goto(a[0]*100-150, 50-a[1]*100)
        self.stamp()
        allpos.remove(a)

    def __go(self):
        self.clear()
        self.goto(0, 0)
        self.shape(bg)
        self.stamp()
        for x in range(4):
            for y in range(4):
                if block2[x][y]:
                    self.goto(x*100-150, 50-y*100)
                    self.shape(f'{rpath}\\{block2[x][y]}.gif')
                    self.stamp()
        self.grow()
    def go_down(self):
        if fin:return
        for i in range(4):
            while any(self.__judge(i, u, i, u + 1) for u in (2, 1, 0)):pass
            #for o in range(3):
            #    if not True in [self.__judge(i, u, i, u + 1) for u in (2, 1, 0)]:break
        self.__go()

    def go_up(self):
        if fin:return
        for i in range(4):
            while any(self.__judge(i, u, i, u - 1) for u in (1, 2, 3)):pass
        self.__go()

    def go_left(self):
        if fin :return
        for u in range(4):
            while any(self.__judge(i, u, i - 1, u) for i in (1, 2, 3)):pass
        self.__go()

    def go_right(self):
        if fin:return
        for u in range(4):
            while any(self.__judge(i, u, i + 1, u) for i in (2, 1, 0)):pass
        self.__go()
    def __judge(self,i,u,y,x):
        global block2, score, top_score
        a, b = block2[i][u], block2[y][x]
        if a == 0:return False
        if b == 0: allpos.remove((y, x))
        elif b == a:
            score += a
            if score > top_score: top_score = score
            if a == 1024: win_lose.show_text("达成2048，继续请按回车键")
        else:return False
        block2[y][x] += a
        block2[i][u] = 0
        allpos.append((i, u))
        return True
    def __check(self):
        for i in range(4):
            for u in range(4):
                b = block2[i][u]
                if b == 0 or u < 3 and (b == block2[i][u+1] or block2[u][i] == block2[u+1][i]):return
        global fin;fin = True
        win_lose.show_text('游戏结束，重新开始请按空格键')

class Background(turtle.Turtle):
    def __init__(self, pos):
        super(Background, self).__init__()
        self.pu();self.ht()
        self.color('white')
        self.goto(pos)

    def show_msg(self, pos, msg):
        self.clear()
        self.write(f'{msg}', align='center', font=("Arial", 20, "bold"))

class WinLose(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.pu();self.ht(); self.color('red')
    def show_text(self, text):
        self.write(text, align='center', font=("黑体", 20, "bold"))
        block.grow()

def init():
    global score, allpos, block, block2, fin, pit, TIME
    score, pit = 0, -1
    if fin:
        fin = False; TIME = -1
    else:TIME = 0
    block2 = [[0]*4 for i in range(4)]
    allpos = [(i, u) for i in range(4) for u in range(4)]
    win_lose.clear()
    block = Block()

def draw_time():
    global TIME
    if fin:return
    TIME += 1
    bc_time.show_msg('time', TIME)
    boundary.ontimer(draw_time, 996)

fin = False
pit, TIME, score, top_score = -1, -1, 0, 0
allpos = [(i, u) for i in range(4) for u in range(4)]
block2 = [[0]*4 for i in range(4)]
bc_pit = Background((-115, 210))
bc_time = Background((-115, 135))
bc_score = Background((125, 210))
bc_top_score = Background((125, 135))
block = Block()
win_lose = WinLose()
boundary.listen()
boundary.onkey(block.go_right, 'Right')
boundary.onkey(block.go_left, 'Left')
boundary.onkey(block.go_up, 'Up')
boundary.onkey(block.go_down, 'Down')
boundary.onkey(win_lose.clear, 'Return')
boundary.onkey(init, 'space')
boundary.onkey(boundary.bye, 'Escape')
if __name__ == '__main__':
    boundary.update()
    boundary.mainloop()
