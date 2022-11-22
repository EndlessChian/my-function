#!usr/bin/env pytohn
# coding = utf-8
import cv2 as cv
from PIL import Image
import time
import shutil
import os
'''try:
    from numpy import fromfile, uint8
except ImportError:
    raise ImportWarning("Can't for Chinese in the path because could not get numpy.")
'''
class BIGGER:
    def __init__(self, DATA, afterName=None, Save=True, Filter=None):
        self._filter = ['', ''] if Filter is None else Filter
        if not os.path.isfile(DATA):
            raise self.__exit__(FileNotFoundError, 'Not exist ' + DATA)
        if Save:
            self.IMG = Image.open(DATA)###
            self.IMG.load()###
        ext = DATA.split('.')
        self.file = ext[0] + '\\'
        self.afterName = afterName if afterName else '_HD.'.join(ext)
        if not os.path.exists(self.file):
            os.mkdir(self.file)
        self.src = cv.imread(DATA)  # Chinese is not allowed...
        if self.src is None:
            base, i = 'working_', 0
            while os.path.exists(base+str(i)+'.'+ext[1]): i += 1
            rpath = os.path.realpath(base + str(i)+'.'+ext[1])
            if Save:
                self.IMG.save(rpath)###
            else:
                os.rename(DATA, rpath)#
            print(rpath)
            self.TrueName = rpath
            print(self.src)
            self.src = cv.imread(rpath)
            if self.src is None:
                self.__exit__()
                raise NotImplementedError('Chinese is not allowed.')
            if not Save:self.IMG = Image.open(rpath)#
        else:
            self.TrueName = None
            if not Save:self.IMG = Image.open(DATA)#
        self.y, self.x = self.src.shape[:2]
        self.List_elements = []

    def __enter__(self):
        print('Start...'.center(50, '#'))
        return self

    def read(self, x, y):
        for Y in range(y):
            if int(len(self.List_elements)) > 1:
                self.List_elements.clear()
            for X in range(x):
                # IMG.getpixel((a, b))
                self.List_elements += [list(self.IMG.getpixel((X, Y)))]
            with open(self.file + str(Y), 'w', encoding='utf-8') as f:
                f.write(str(self.List_elements))
                f.flush()

        time.sleep(2)

    def bigger(self, x, y, Multiple):
        if self._filter[0] and self._filter[0] != '4':
            self.allFilter(self._filter[0])
        result = cv.resize(self.src, (x * Multiple, y * Multiple))

        for RGB_Y in range(y):
            data = eval(open(self.file + str(RGB_Y), encoding='utf-8').read())
            M_y = Multiple * RGB_Y
            for RGB_X in range(x):
                _ = data[RGB_X].reverse()
                M_x = Multiple * RGB_X

                try:
                    result[M_y:M_y + Multiple, M_x:M_x + Multiple] = _
                except:
                    pass

        if self._filter[1] and self._filter[1] != '4':
            cv.imwrite(self.TrueName, self.allFilter(self._filter[1], result)) if self.TrueName else \
            cv.imwrite(self.afterName, self.allFilter(self._filter[1], result))
        else:
            cv.imwrite(self.TrueName, result) if self.TrueName else cv.imwrite(self.afterName, result)

    def close(self):
        try:
            if self.TrueName: os.rename(self.TrueName, self.afterName)
            shutil.rmtree(self.file)
        except Exception as e:
            print(e)

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        print(exc_type, exc_val, exc_tb) if exc_type else print('End...'.center(50, '#'))
        self.close()

    def boxFilter(self, data=None, boxsize: tuple[int, int]=None):
        if boxsize is None: boxsize = ((self.y // 100) | 1, (self.x // 100) | 1)
        if not all(boxsize):return
        if not data is None:
            return cv.boxFilter(data, -1, boxsize, normalize=1)
        self.src = cv.boxFilter(self.src, -1, boxsize, normalize=1)

    def GaussFilter(self, data=None, boxsize: tuple[int, int] = None):
        if boxsize is None: boxsize = ((self.y // 150) | 1, (self.x // 150) | 1)
        if not all(boxsize):boxsize = (1, 1)
        if not data is None:
            return cv.GaussianBlur(data, boxsize, 0)
        self.src = cv.GaussianBlur(self.src, boxsize, 0)

    def midFilter(self, data=None, size: int=0):
        if not size: size = (min(self.x, self.y) // 150) | 1
        if not data is None:
            return cv.medianBlur(data, size)
        self.src = cv.medianBlur(self.src, size)

    def allFilter(self, f, data=None, boxsize=None):
        match f:
            case '0' | 'box':
                return self.boxFilter(data, boxsize)
            case '1' | 'gas':
                return self.GaussFilter(data, boxsize)
            case '2' | 'med':
                return self.midFilter(data, boxsize)
        return data



def webpTOjpg(*images, save=True):
    for img in images:
        ind = img.rfind('.')
        if img[ind:] != '.webp': continue
        print(img)
        print('Start...'.center(50, '#'))
        data = Image.open(img)
        data.load()
        path = img[:ind] + '.jpg'
        data.save(path)
        if not save:
            os.remove(path)
        print('End...'.center(50, '#'))


def walk(dir, ext='.jpg', deepth=1):
    for r, d, f in os.walk(dir):
        deepth -= 1
        #yield from map(lambda i: os.path.join(r, i), filter(lambda i: os.path.splitext(i)[1] == ext, f))
        yield from [os.path.join(r, i) for i in f if os.path.splitext(i)[1] == ext]
        if not deepth:break

def loop(DATA, Multiple, Save=True, Filter=None):
    with BIGGER(DATA, Save=Save, Filter=Filter) as bigger:
        x, y = bigger.x, bigger.y
        bigger.read(x, y)
        bigger.bigger(x, y, Multiple)


if __name__ == '__main__':
    while (DATA := input("Image's path:Chinese is not allowed...")):
        Multiple = int(input('x:>1 and integer...'))
        Save = input('y/n')[0].lower() == 'y'
        extpos = DATA.rfind('.')
        to_loop = lambda : loop(DATA, Multiple, Save, Filter = input('box: 0 | gas: 1 | med: 2 | False: 4 First and duble Filter(space)').split())
        if extpos == -1:
            if os.path.exists(DATA):
                for f in walk(DATA):
                    if (x := input(f+'continue'.center(50, '#')).lower()) in ('y', '', '\n'):
                        DATA = f
                        to_loop()
                    elif x == 'q':
                        break
        elif DATA[extpos:] == '.webp':
            webpTOjpg(DATA, save=input(DATA+'\n\tIt is webp picture and need to change into jpg. Do you want to keep the before one?'))
            DATA = DATA[:extpos] + '.jpg'
            to_loop()
        else:
            to_loop()
