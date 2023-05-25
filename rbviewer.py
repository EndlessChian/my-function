#!python3
#coding=utf-8
import numpy as np
from time import sleep
from io import StringIO
from os import system
from sys import platform
CLEAR = 'cls' if platform.startswith('win') else 'clear'

class rb8reader:
    @staticmethod
    def read_head(file) -> ('heigth', 'width', 'fps', 'fill'):
        file.seek(0, 0)
        se = bytearray(file.read(3))
        se = (se[0] + 1) * 8, se[1] + 1, (se[2] >> 1) + 1, se[2] & 1
        return se

    def __init__(self, file, io, se, arg):
        self.file = file
        if se:
            self.revert_size = se[0], se[1] # heigth, width
            self.fps = 1 / se[2]            # frame pre second
            self.arr = np.full(self.revert_size, not not se[3], dtype=bool) # fill
            self.gate = arg.gate or arg.start * se[2]
            self.rear = arg.rear or arg.stop * se[2]
        else:
            self.revert_size = self.read_size(file)
            self.gate = arg.gate
            self.rear = arg.rear
        self.c = 0                      # frame
        self.jump = 0
        self.JUMP = arg.jump
        self.replay = 0
        self.REPLAY = arg.replay
        assert (not self.rear or self.rear > self.gate), \
            'Can\'t play a frame because of not a positive integer!'
        self.SLEEP = not(self.gate or arg.breakpoint)
        self.breakpoint = arg.breakpoint
        if io:
            self.io = io
            self.out = np.empty_like(self.arr, dtype=bytes) if arg.out else None

    def __call__(self, int) -> bool:
        self.c += int
        if self.SLEEP:sleep(int * self.fps)
        elif self.c >= self.gate:
            if self.breakpoint:
                b = input('breakpoint frames: %d' % self.c)
                if b:
                    if b == 'b': self.REPLAY = 0; return True
                    if b == 'r': self.REPLAY = self.replay + 1; return True
                    if b == 's': self.SLEEP = True
            else: self.SLEEP = True
        else:
            if self.rear and self.c >= self.rear: return True
        return False

    def read_count_normal_mode(self) -> (int, bool):
        a = ord(self.file.read(1))
        if a and a != 255: return a, True
        b = ord(self.file.read(1))
        if b != 255:       return a + b, not not a
        r = not not a
        a += b
        while 1:
            a += (b := ord(self.file.read(1)))
            if b != 255:   return a, r

    def read_count_double_revert_mode(self) -> (int, bool):
        a = 0
        self.revert = not self.revert
        while 1:
            a += (b := ord(self.file.read(1)))
            if b != 255: return a, self.revert

    def match(self, mode) -> bool:
        if mode == b'\x00':   return self(1)
        elif mode == b'\x01': self.arr.fill(False); return self.play()
        elif mode == b'\x02': self.arr.fill(True); return self.play()
        elif mode == b'\x03': return self(self.read_count_normal_mode()[0])
        elif mode == b'\x05': self.arr = (self.arr == False); return self.play()
        elif mode == b'\x0b' or mode == b'\x0c':
            y, x = bytearray(self.file.read(2))
            y *= 8
            self.revert = False
            method = self.read_count_normal_mode if mode == b'\x0c' else self.read_count_double_revert_mode
            while 1:
                l, r = method()
                if r:
                    data = np.array(bytearray(self.file.read(l)), dtype=np.uint8)
                    l0  =  self.revert_size[1] - x
                    for i in range(8):
                        I = 2 ** i & data != 0
                        if l <= l0:         # x == width is aceptable
                            self.arr[y + i, x : l + x] = I
                        else:
                            self.arr[y + i, x:]    =     I[:l0]
                            for u in range(l0, l, self.revert_size[1]):
                                i += 8
                                self.arr[y + i, : l - u] = I[u: u + self.revert_size[1]]

                    if l < l0: x += l       # x == width would not happend
                    else:
                        x = l - l0; y += 8
                        while x >= self.revert_size[1]:     # x == width would not happen
                            x -= self.revert_size[1]; y += 8
                else:
                    if l:
                        x += l
                        while x >= self.revert_size[1]:     # x == width would not happen
                            x -= self.revert_size[1]; y += 8
                    else: return self.play()
        elif mode == b'\x11':
            data = ord(self.file.read(1)) & 2 ** np.arange(8)
            data.resize((8, 1))
            for i in range(0, self.revert_size[0], 8): self.arr[i: i + 8, :] = data
            return self.play()
        elif mode == b'': return True
        else:assert 0, (mode, self.file.tell())
        return False

    @staticmethod
    def write_count(int) -> bytearray:
        a, b = divmod(int, 255)
        return bytearray((255,) * a + (b,))

    def play(self) -> False:
        if self.JUMP:
            self.jump += 1
            if self.jump == self.JUMP: self.jump = 0
            else: return
        if self.out is not None:        # print to a filelike so can see it in others way visiable
            self.out.fill(b'@') # 0x4d
            np.place(self.out, self.arr, b' ') # 0x20
            for i in self.out: self.io.write(i.tobytes('A')); self.io.write(b'\n')
            # self.io.write(self.write_count()) #write sleep frames, just use read_count to read it
            self.io.write(b'\n')
        else:
            system(CLEAR)
            self.io.seek(0, 0)
            for i in range(self.revert_size[0]):
                for u in range(self.revert_size[1]):
                    self.io.write('\033[7m \033[0m' if self.arr[i, u] else ' ')
                self.io.write('\n')

            print(self.io.getvalue(), end='')
        return False

    def loop(self) -> int:
        while 1:
            while 1:
                if self.match(self.file.read(1)): break
            if self.REPLAY:
                if self.replay == self.REPLAY: break
                else: self.c = 0; file.seek(3)
                self.replay += 1
            else: break
        return self.c

    def mask_print(self) -> bool:
        for i in range(self.revert_size[0]):
            print(self.file.readline().decode('utf-8').replace('@', '\033[7m \033[0m'), end='')

        self(1)# self(self.read_count()) # can't count sleep frames yet
        return not self.file.read(1)     # sep between frames is '\n'

    def mask_show(self) -> int:
        while 1:
            while 1:
                if self.mask_print(): break
            if self.REPLAY:
                if self.replay == self.REPLAY: break
                self.c = 0
                file.seek(0, 0)
                self.replay += 1
            else: break
        return self.c

    @staticmethod
    def read_size(file) -> ('height', 'width'):
        file.seek(0)
        b = len(file.readline())
        a = 0
        while b == len(file.readline()) > 1: a += 1
        file.seek(0)
        return a, b


class rb16reader:
    pass


def screen_resize(size):
    return system('mode con cols={} lines={}'.format(*size))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help='path of the raw-binary file ')
    parser.add_argument('-g', '--gate', required=False, help='the frame to start play ', type=int, default=0)
    parser.add_argument('-s', '--start', required=False, help='the second to start play ', type=int, default=0)
    parser.add_argument('-e', '--rear', required=False, help='the frame to interrupt in ', type=int, default=0)
    parser.add_argument('-t', '--stop', required=False, help='the second interrupt in ', type=int, default=0)
    parser.add_argument('-r', '--replay', required=False,
                        help='times to replay before finishing, or send -1 to replay forever ', type=int, default=0)
    parser.add_argument('-b', '--breakpoint', action='store_true', help='a breakpoint to control the step ')
    parser.add_argument('-v', '--vision', help='the vision need to read as ', required=False)
    parser.add_argument('-o', '--out', required=False, help='the path to save the screenshot ')
    parser.add_argument('-m', '--mask', action='store_true', help='show the compeleted text(which used -o to collect) ')
    parser.add_argument('-j', '--jump', required=False, help='jump some frames so make the file smaller ', type=int, default=0)
    args = parser.parse_args()
    with open(args.path, 'rb') as file:
        if args.vision:
            assert (rb := args.vision.lower()) in ('rb8', 'rb16', '8', '16'), 'Not support vision!'
            PLAYER = (rb8reader if rb in ('rb8', '8') else rb16reader)
        else:
            assert (rb := args.path.split('.')[-1].lower()) in ('rb8', 'rb16'), 'Not support vision!'
            PLAYER = (rb8reader   if  rb == 'rb8'   else   rb16reader)

        if not args.mask:
            header = PLAYER.read_head(file)
            with open(args.out, 'wb') if args.out else StringIO() as out:
                player = PLAYER(file, out, header, args)
                if not args.out: screen_resize((header[1], header[0]))
                print(header)
                player.loop()#python D:/python/Lib/site-packages/.work/rbviewer.py -p "D:/picture/Video/Bad Apple.rb8" -b

        else:
            player = PLAYER(file, None, None, args)
            player.mask_show()
        #python D:/python/Lib/site-packages/.work/rbviewer.py -p "D:/picture/Screenshot_2022-04-03-13-24-25.txt" -b -m -v "rb8"
