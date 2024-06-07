from PIL import Image
import numpy as np
import os
"""
    'BOOL': ('1', 1),
    'GREYB': ('L', 8),
    'GREYI': ('I', 32),
    'GREYF': ('F', 32),
    'MAP': ('P', 8),
    'RGB': ('RGB', 8 * 3),
    'RGBA': ('RGBA', 8 * 4), # only .png
    'PRINT': ('CMYK', 8 * 4),# green, red, yellow, black
    'BRIGHT': ('YCbCr', 8 * 3)
"""
class IMGStruct:
    def __init__(self, img: Image, arr=None):
        self.img = img
        img.load()
        self.arr = np.asarray(img) if arr is None else arr
    def __enter__(self): return self
    def __exit__(self, tp, arg, evt):
        self.img.close()
        self.img = self.arr = None

    def close(self): self.__exit__(None, '', 0)

    @staticmethod
    def mapRGBgreyb(img, rgb):
        new = IMGStruct(Image.new('L', img.img.size), mapRGBgreyb(img.arr, rgb))
        new.arr.resize(new.arr.size)
        new.img.putdata(new.arr)
        new.arr.resize(new.img.size)
        return new

    @staticmethod
    def mapGREYBbin(img, mid: int):
        new = IMGStruct(Image.new('1', img.img.size), mapGREYBbin(img.arr, mid))
        new.arr.resize(new.arr.size)
        new.img.putdata(new.arr)
        new.arr.resize(new.img.size)
        return new

    def save(self, path, *args, **kwargs):
        size = self.arr.shape
        self.arr.resize(self.arr.size)
        self.img.putdata(self.arr)
        self.arr.resize(size)
        self.img.save(path, *args, **kwargs)


def mapRGBgreyb(arr: np.array, rgb=(1, 1, 1)) -> np.uint8:
    return np.uint8( np.around( np.median( arr * rgb, axis=2 ) ) )

def mapGREYBbin(arr: np.array, mid: int):
    resver_size = arr.shape[1], arr.shape[0] // 8
    arr = np.uint8( arr > mid ).T.reshape( (resver_size[0] * resver_size[1], 8) )
    for i in range(1, 8):
        arr[:, i] >>= i
    return arr.sum(axis=1, dtype=np.uint8).reshape( resver_size ).T

'''
:condition
0 <= a < b <= 255
0 <= q <= 1
0 <= p, c1, c2 <= 255
:principle
c1 = p*q + a(1 - q)
c2 = p*q + b(1 - q)
:solve
q = 1 - (c2 - c1) / (b - a)
p = (b * c1 - a * c2) / [(b - a) - (c2 - c1)]
:depart
c1 <= c2
c2 - c1 <= b - a
b * c1 >= a * c2
:system
c1 = H1[c1'] = k * c1' + e1
c2 = H2[c2'] = k * c2' + e2
:inequality limit
&a = min{c2' - c1'} = (e1 - e2) / k
&b = max{c2' - c1'} = (b - a) / k + &a
&f = min{b * c1 - a * c2} = (a * e2 - b * e1) / k
:solve equation
k = (b - a) / (&b - &a)
e1 = k * (&f + a * &a) / (a - b)
e2 = k * (&f + b * &a) / (a - b)
:judgment
k ~= 0.5
e1 ~= 0.
e2 ~= 127.5
:warn

'''
def phantom_tank(new: IMGStruct, img0: IMGStruct, img1: IMGStruct, bk0=0, bk1=255):
    """:TODO: Misk two grey image into one RGBA photo, the color can change because backgroung translate(in grey).
    new: RGBA format Image IMGStruct. It's data did not cause any different to the result
    img0: L format Image IMGStruct. Image want to show when background with a color of bk0
    img1: L format Image IMGStruct. Image want to show when backgroung with a color of bk1
    bk0: Integer. defalut with 0
    bk1: Integer. defalut with 255
    :NOTES:
    * backgroung only have one simple color and significant. 0 <= bk0 << bk1 <= 255
    * All images parameters have the same photo size. if necessery, using function paste_image()
       transform images into a same size
    * Only support show out grey color, split the RGB photo to select a best alpha as input
    """
    assert bk0 < bk1, "If what to get such a different background, Please switch image 0 and image 1"
    assert img0.img.size == img1.img.size == new.img.size
    arr0 = np.int32(img0.arr)
    arr1 = np.int32(img1.arr)
    arrdx = arr1 - arr0
    c_min = arrdx.min()     # (e1 - e2) / k
    c_max = arrdx.max()     # (b - a) / k + c_min
    d_min = (bk1 * arr0 - bk0 * arr1).min()     # (a * e2 - b * e1) / k
    k = (bk1 - bk0) / (c_max - c_min)
    e1 = k * (d_min + bk0 * c_min) / (bk0 - bk1)
    e2 = k * (d_min + bk1 * c_min) / (bk0 - bk1)
    arr0 = np.int16(np.around(np.multiply(arr0, k, dtype=float) + e1))
    arr1 = np.int16(np.around(np.multiply(arr1, k, dtype=float) + e2))
    print(c_min, c_max, d_min)  #-142 254 -7620
    print(k, e1, e2)
    # print(arr0)
    # print(arr1)
    w = (bk1 - bk0) - (arr1 - arr0)
    q = np.around(np.multiply(w, 255 / (bk1 - bk0), dtype=float))
    # print(q, (q > 255).any(), (q < 0).any())
    "never used np.put !!!!"
    q = q.astype(np.uint8, copy=False)#np.uint8(q)
    zero = w == 0
    w[zero] = 1
    p = np.around((np.multiply(bk1, arr0, dtype=np.int32) - bk0 * arr1) / w)
    p[p > 255] = 255
    p[p < 0] = 0
    p = np.uint8(p)
    p[zero] = 255

    a = Image.new('L', new.img.size)
    b = Image.new('L', new.img.size)
    q.resize(q.size)
    p.resize(p.size)
    try:
        a.putdata(p)
        b.putdata(q)
        "never used new.img.paste(a, mask=b)   !!!!"
        new.close()
        new.img = Image.merge('RGBA', (a, a, a, b))
    finally:
        a.close()
        b.close()
    return new.img

def paste_image(img, background, center=(0, 0)):
    assert (img.img.size[0] <= background.img.size[0] and img.img.size[1] <= background.img.size[1])
    center = (background.img.size[0] - img.img.size[0] >> 1) + center[0], (background.img.size[1] - img.img.size[1] >> 1) + center[1]
    center = center[0], center[1]
    # print(img.img.size, background.img.size, center)
    background.img.paste(img.img, box=center, mask=img.img.split()[3] if img.img.mode == 'RGBA' else None)
    background.arr = np.asarray(background.img)

if __name__ == "__main__":
    path0 = r'D:\picture\EditedPhotos\Screenshot_2022-01-27-11-34-22.jpg'
    path1 = r'D:\picture\EditedPhotos\Screenshot_2022-01-27-13-31-44.jpg'
    assert os.path.isfile(path0) and os.path.isfile(path1)
    dir0 = os.path.dirname(path0)
    dir1 = os.path.dirname(path1)
    with IMGStruct(Image.open(path0)) as img0:
        arr0s = img0.img.split()
        name0 = os.path.splitext(path0)
        for i in range(len(arr0s)):
            with IMGStruct(arr0s[i]) as img0i:
                img0i.save(os.path.join(dir0, f'{name0[0]}-alpha-{i}{name0[1]}'))

    with IMGStruct(Image.open(path1)) as img1:
        arr1s = img1.img.split()
        name1 = os.path.splitext(path1)
        for i in range(len(arr1s)):
            with IMGStruct(arr1s[i]) as img1i:
                img1i.save(os.path.join(dir1, f'{name1[0]}-alpha-{i}{name1[1]}'))

    # path0 = r'D:\picture\EditedPhotos\Screenshot_2022-01-27-11-34-22-alpha-1.jpg'
    # path1 = r'D:\picture\EditedPhotos\Screenshot_2022-01-27-13-31-44-alpha-0.jpg'
    # assert os.path.isfile(path0) and os.path.isfile(path1)
    # dir0 = os.path.commonpath((path0, path1))
    # a = 0
    # b = 245
    # with IMGStruct(Image.open(path0)) as img0:
    #     with IMGStruct(Image.open(path1)) as img1:
    #
    #         size = max(img0.img.size[0], img1.img.size[0]), max(img1.img.size[1], img0.img.size[1])
    #         with IMGStruct(Image.new('L', size), 0) as img0n:
    #             with IMGStruct(Image.new('L', size), 0) as img1n:
    #                 paste_image(img0, img0n)
    #                 paste_image(img1, img1n)
    #
    #                 with IMGStruct(Image.new('RGBA', size)) as new:
    #                     phantom_tank(new, img0n, img1n, a, b)
    #                     new.img.save(os.path.join(dir0,
    # f'{os.path.splitext(os.path.basename(path0))[0]}-{os.path.splitext(os.path.basename(path1))[0]}.png')
    #                                 )


