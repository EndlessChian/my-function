import numpy as np
from _cfunc import _graphics

def center_map2(arr):
    assert arr.shape[0] == arr.shape[1]
    k = int(np.ceil(arr.shape[0] / 2))
    for i in range(k):
        for j in range(i, k):
            arr[j, i] = arr[i, j]
    # for j in range(k):
    #     arr[0: k, -1 - j] = arr[0: k, j]
    arr[0:k:1, k-1::1] = arr[0:k:1, k-1::-1]
    # for i in range(k):
    #     arr[-1 - i] = arr[i]
    arr[k-1::1] = arr[k-1::-1]
    return arr


edge_kernel = center_map2(np.array(
    [
        [7,  2, 2,  0, 0],
        [0, -7, -6, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0,  0,  0]
    ], dtype=np.int8
))

def edge_cov(arr: np.ndarray):
    if arr.ndim == 2:
        return convolution(arr, edge_kernel)
    elif arr.ndim == 3:
        out = np.empty_like(arr)
        li = np.array_split(arr, axis=2)
        for ch, a in enumerate(li):
            out[..., ch] = convolution(a, edge_kernel)
        return out

def distance(arr1: np.ndarray, arr2: np.ndarray):
    if not isinstance(arr1, np.ndarray):
        arr1 = np.array(arr1, dtype=np.float32)
    elif arr1.dtype != np.float32:
        arr1 = arr1.astype(np.float32)
    if not isinstance(arr2, np.ndarray):
        arr2 = np.array(arr2, dtype=np.float32)
    elif arr2.dtype != np.float32:
        arr2 = arr2.astype(np.float32)
    if arr1.shape != arr2.shape:
        raise ValueError("Must has the same shape.")
    out = np.empty_like(arr1, dtype=np.uint8)
    _graphics.distance(arr1, arr2, out)
    return out

def convolution(arr: np.ndarray, kernel: np.ndarray):
    if not isinstance(arr, np.ndarray):
        raise TypeError("Not a ndarray type.")
    if not isinstance(kernel, np.ndarray):
        kernel = np.array(kernel, dtype=np.int8)
    if not (arr.dtype == np.uint8):
        raise TypeError("Not a bytes array.")
    out = np.empty_like(arr, shape=(arr.shape[0] - kernel.shape[0] + 1, arr.shape[1] - kernel.shape[1] + 1))
    _graphics.convolution(arr, kernel, out)
    return out

def verification(arr, kernel):
    print(arr)
    print(kernel)
    out = distance(arr, arr)
    print(out)
    new = np.sqrt(2. * arr * arr).astype(np.uint8)
    print(new)
    print((out == new).all())
    out = convolution(arr, kernel)
    arr = (arr - 128).astype(np.int8).astype(np.int32)
    new = np.empty((arr.shape[0] - kernel.shape[0] + 1, arr.shape[1] - kernel.shape[1] + 1), dtype=np.uint8)
    tab = np.empty(new.shape[1], dtype=np.int32)
    for i in range(len(new)):
        tab.fill(kernel.size // 2)
        for j in range(len(kernel)):
            tab += np.convolve(arr[i + j], kernel[-1-j], 'valid')
        new[i] = (tab // kernel.size) + 128
    print(new)
    print(out)
    print((new == out).all())

# verification(np.arange(16, dtype=np.uint8).reshape((4,4)),
#                  np.array([-1,1,-1,-1], dtype=np.int8).reshape((2,2))
#       )

'''
1 2 3
1 2 3
1 2 3

-1 1
-1 1
'''