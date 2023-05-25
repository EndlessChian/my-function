#!python3
#coding=utf-8
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as IMG
import io
"""
    'BOOL': ('1', 1),
    'GREYB': ('L', 8),
    'GREYI': ('I', 32),
    'GREYF': ('F', 32),
    'MAP': ('P', 8),
    'RGB': ('RGB', 8 * 3),
    'RGBA': ('RGBA', 8 * 4),
    'PRINT': ('CMYK', 8 * 4),# green, red, yellow, black
    'BRIGHT': ('YCbCr', 8 * 3)
"""

class IMGStruct():
    def __init__(self, img: Image, arr=None):
        self.img = img
        img.load()
        self.arr = np.asarray(img) if arr is None else arr
    def __enter__(self): return self
    def __exit__(self, tp, arg, evt):
        self.img.close()
        self.img = self.arr = None

    def close(self): self.__exit__(None, '', 0)

    def imshow(self, name=None):
        try:
            cv2.imshow(name or str(self), self.arr)
            while cv2.waitKey(50) & 0xff != ord('q'): pass
        except Exception as e: self.close()
        finally: cv2.destroyAllWindows()

    @staticmethod
    def mapRGBgrey(img):
        new = IMGStruct(Image.new('L', img.img.size))
        new.arr = mapRGBgrey(img.arr)
        new.putdata(new.arr)
        return new

    @staticmethod
    def mapRGBbin(img, mid: int):
        new = IMGStruct(Image.new('1', img.img.size))
        new.arr = mapRGBbin(img.arr, mid)
        new.putdata(new.arr)
        return new


class MBPStruct:
    def __init__(self, size):
        self.img = Image.new('1', size)
        self.resver_size = size[1], size[0] // 8
        self.length = self.resver_size[0] * self.resver_size[1]
        self.io = io.BytesIO()

    def __enter__(self): return self
    def __exit__(self, tp, val, tb):
        self.img.close()
        self.io.close()
        self.io = self.img = self.arr = None

    def mapGREYbin(self, grey, mid: int):
        arr = np.uint8( grey > mid ).T.reshape( (self.length, 8) )
        for i in range(1, 8): arr[:, i] >>= i
        arr = arr.sum(axis=1, dtype=np.uint8).reshape( self.resver_size ).T.reshape( self.length )
        self.img.putdata(arr)
        return arr

    def tobytes(self) -> io.BytesIO:
        self.io.seek(0, 0)
        self.io.flush()
        self.img.load()
        # unpack data
        e = Image._getencoder(self.img.mode, 'raw', self.img.mode)
        e.setimage(self.img.im)
        bufsize = max(65536, self.img.size[0] * 4)  # see RawEncode.c

        while True:
            l, s, d = e.encode(bufsize)
            self.io.write(d)
            if s: break
        if s < 0: raise RuntimeError(f"encoder error {s} in tobytes")
        return self.io


class CAPTUREStruct:
    def __init__(self, path: str or int, size=None, fps=0, fourcc=0):
        self.video = cv2.VideoCapture(path)
        assert self.video.isOpened()
        self.size = size or int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if size:
            self.video.set(3, size[0])
            self.video.set(4, size[1])

        self.fps = fps or int(self.video.get(cv2.CAP_PROP_FPS))
        if fps: self.video.set(5, fps)
        self.fourcc = fourcc or int(self.video.get(cv2.CAP_PROP_FOURCC))
        if fourcc: self.video.set(6, fourcc)

    def read(self) -> (bool, np.array):
        try:
            assert self.video.isOpened()
            return self.video.read()
        except Exception as e:
            self.close()
            raise e

    def __enter__(self): return self

    def __exit__(self, tp, val, tb):
        self.video.release()
        self.video = None

    def close(self): self.__exit__(None, '', 0)


class VIDEOStruct:
    def __init__(self, path, fourcc: str, fps: int, size: tuple):
        self.video = cv2.VideoWriter()
        self.video.open(path, fourcc, fps, size, True)
        self.fourcc, self.size, self.fps = fourcc, size, fps

    def write(self, frame):
        try:
            assert self.video.isOpened()
            self.video.write(frame)
        except Exception as e:
            self.close()
            raise e

    def close(self): self.__exit__(None, '', 0)

    def __enter__(self): return self
    def __exit__(self, tp, val, tb):
        self.video.release()
        self.video = None
    __del__ = close


def mapRGBgrey(arr: np.array) -> np.uint8:
    return np.uint8( np.around( np.median( arr, axis=2 ) ) )

def mapRGBbin(arr: np.array, mid: int):
    resver_size = arr.shape[1], arr.shape[0] // 8
    arr = np.uint8( np.median( arr, axis=2 ) > mid ).T.reshape( (resver_size[0] * resver_size[1], 8) )
    for i in range(1, 8):
        arr[:, i] >>= i

    return arr.sum(axis=1, dtype=np.uint8).reshape( resver_size ).T

def mapMP4grey(video: CAPTUREStruct, new: VIDEOStruct) -> int:
    refer = video.size
    host = new.size
    i, j = divmod(refer[0], host[0])
    o, u = divmod(refer[1], host[1])
    c = 0
    while 1:
        tr, fr = video.read()
        if tr: new.write( mapRGBgrey(fr[j : : i, u : : o]) )
        else:  return c
        c += 1

'''
:sys:
0 : sleep + sys
1 : fill 0 + sys
2 : fill 1 + sys
3 : still + fps
4 : replay + times-1 + frame-1      /not yet
5 : revert + sys
6 : rect_fill_0 x1 + y1 + x2 + y2   /not yet
7 : rect_fill_1 x1 + y1 + x2 + y2   /not yet
8 : rect_revert x1 + y1 + x2 + y2   /not yet
9 : circle_fill_0 x + y + r         /not yet
a : circle_fill_1 x + y + r         /not yet
b : double_revert x + y + l + data + l + l + data +...+ 0 + sys    /when blocks have a far instance, normal_map can simplify like this
c : normal_map  x + y + l + data +...+ 0 + l + l + data +...+ 0 + 0 + sys
d : revert_map  x + y + l + data +...+ 0 + l + l + data +...+ 0 + l + -1 + l +...+ 0 + 0 + sys    /not yet
e : single_map  x + y + l + data + sys
f : short_fill  l + fill + ...      /not end, used in assisting others mode, restep in front mode after filling
10: long_fill   n + x + y + fill + x + y + fill +...+ sys   /not yet
11: fill  fill + sys
'''
def mapMP4rb8(video: CAPTUREStruct, file: open, size, fps=30, mid=127) -> int:
    refer = video.size
    i, j = divmod(refer[1], size[0])
    o, u = divmod(refer[0], size[1])
    c = 0
    revert_size = size[1], size[0] // 8
    se = bytearray((
        revert_size[1] - 1,# height/8 - 1
        size[1] - 1,       # width - 1
        fps - 1 << 1,      # fps -1 : 7 | fill : 1
                           # sys
    ))
    file.write(se)
    x = l = 0
    length = revert_size[0] * revert_size[1]
    arr0 = np.zeros(length, dtype=bool)
    frame0 = np.zeros(size, dtype=np.uint8)
    se.clear()
    eq = i == 1 == o and j == 0 == u
    def add_hand(d):   # add y + x or l
        if se:
            a, b = divmod(d, 255)
            for _ in range(a): se.append(255)
            se.append(b)
        else:se.extend(divmod(d, size[1]))

    def long_false_add():
        nonlocal l
        data = arr[x - l : x]
        #if len(data) > 5 and (data == data[0]).all():
        #    se.append(0)
        #    se.append(0)
        #    se.append(15)
        #    add_hand(l)
        #    se.append(data[0])
        #else:
        add_hand(l)
        se.extend(data)
        l = 0

    def long_true_add():
        nonlocal l
        #se.append(0)
        #if l > 255 * 4 - 1:     # too long not change, force to make a new term
        #    se.append(0)
        #    se.append(12)
        #    se.extend(divmod(x, size[1]))
        #else: add_hand(l)
        add_hand(l)
        l = 0

    def count_still():
        nonlocal l
        if l == 1:file.write(b'\x00')
        else:
            a, b = divmod(l, 255)
            file.write(b'\x03')
            if a:file.write(b'\xff' * a)
            file.write(bytearray((b,)))
        l = 0

    while 1:
        tr, frame = video.read()
        if not tr: return c     # count frames
        c += 1
        frame = mapRGBgrey(frame if eq else frame[j :: i, u :: o])
        tr = np.isclose(frame, frame0, atol=20)
        if tr.all():   # match stilling frames
            l += 1; continue
        elif l: count_still(); continue
        else: frame0 = frame

        arr = (frame > mid if type(mid) == int else mid(np.median(frame))).T.reshape((length, 8))
        if arr.all():     file.write(b'\x02'); continue # match fill 1
        if not arr.any(): file.write(b'\x01'); continue # match fill 0
        if not tr.any():  file.write(b'\x05'); continue # match revert frame
        arr = np.uint8(arr)
        for x in range(1, 8): arr[:, x] <<= x
        arr = arr.sum(axis=1, dtype=np.uint8).reshape(revert_size).T.reshape(length)  # change the form of data
        tr = iter(arr == arr0)      # size: length
        arr0 = arr

        for x in range(length): # get start position
            if not next(tr): break
        else:l += 1; continue  # this case not change too, break to next frame

        if l: count_still(); l = 0
        # assert not l and not se   # under normal map mode, a term only have one start position
        add_hand(x)
        equal = False
        for x in range(x + 1, length):  # match data and count l
            l += 1
            if next(tr):
                if not equal:
                    equal = True
                    long_false_add()
            elif equal:
                long_true_add()# if l > 5 else long_false_add()  # too short to long jump(normal mode)
                equal = False
        if l and not equal: long_false_add()
        l = 0
        file.write(b'\x0b')        # enter double revert map mode
        file.write(se)
        file.write(b'\x00\x00')    # step out last term and turn to next frame
        se.clear()
        file.flush()


path = r"D:\picture\Video\Bad Apple but it's in 4k 60fps.mp4"
newpath = r'D:\picture\Video\Bad Apple.rb8'
from time import time
t0 = int(time())
with CAPTUREStruct(path) as cap:
    with open(newpath, 'wb') as new:
        c = mapMP4rb8(cap, new, (64, 128), cap.fps)
        size = new.tell()
t = c // cap.fps
print('Readed', c, 'frames:', t, 's.', 'time', int(time()) - t0, 's', 'size', size, 'b =', size // 1024, 'kb')
# Readed 13142 frames: 219 s. time 45 size 4024541 b = 3930 kb
# Readed 13142 frames: 219 s. time 47 s size 1786671 b = 1744 kb
# raw: 13142 kb -> 3875 kb ~= 30%

def mapBINgrey(arr):pass

def rb8shower(file):
    se = bytearray(file.read(3))
    revert_size = 8 * (se[0] + 1), se[1] + 1
    se = (se[2] >> 1) + 1
    print('height:', revert_size[0], '; width:', revert_size[1], '; fps:', se)
    fps = 1 / se
    c = 0
    arr = np.zeros(revert_size, dtype=np.uint8)
    from time import sleep, time_ns
    from matplotlib.animation import FuncAnimation
    fig, ax = plt.subplots()

    def read_count():
        a = ord(file.read(1))
        r = not not a
        if r and a != 255:  return a, r
        b = ord(file.read(1))
        if b != 255:        return a + b, r
        a += b
        while 1:
            a += (b := ord(file.read(1)))
            if b != 255:    return a, r

    def match(mode):
        nonlocal c, arr
        print(mode)
        if mode == b'\x00': sleep(fps); c += 1
        elif mode == b'\x01': arr.fill(0)
        elif mode == b'\x02': arr.fill(255)
        elif mode == b'\x03': z = read_count()[0]; sleep(fps * z); c += z
        elif mode == b'\x05': arr = np.uint8(arr == 0) * 255
        elif mode == b'\x12':
            y, x = bytearray(file.read(2))
            y *= 8
            while 1:
                l, r = read_count()
                if r:
                    data = np.array(bytearray(file.read(l)), dtype=np.uint8)
                    print('data',data)
                    l0  =  revert_size[1] - x
                    for i in range(8):
                        if l <= l0:         # x == width is aceptable
                            arr[y + i, x : l + x] = (data & 1) * 255
                        else:
                            arr[y + i, x:]     =a  =       (data[:l0] & 1) * 255;print('arr2',a,end=' ')
                            arr[y + i + 8, : l - l0]=a = (data[l0:] & 1) * 255;print(a)
                        data >>= 1

                    if l < l0: x += l       # x == width would not happend
                    else:      y += 8; x = l - l0
                    plt.imshow(arr);print(l,l0,(y, x))
                else:
                    if l:
                        x += l
                        if x >= revert_size[1]:     # x == width would not happend
                            x -= revert_size[1]
                            y += 8
                    else:return True
                    print(l,(y, x))
        elif mode == b'': input('n'); return ani.pause()
        else:assert 0, (mode, file.tell())

    def show(step):
        nonlocal c
        c += 1
        while match(file.read(1)): plt.imshow(arr)
        plt.imshow(arr)
        return []

    t0 = time_ns()
    ani = FuncAnimation(fig, init_func=lambda : plt.imshow(arr), func=show, frames=180, interval=fps * 1000)
    plt.show()
    return c, c // se
'''
with open(newpath, 'rb') as file:
    c, time = rb8shower(file)
    print('Readed', c, 'frames:', time, 's.')'''