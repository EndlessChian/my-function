from math import factorial, sqrt, log
from array import array
#print((lambda number:eval((lambda: 1 if n == 1 else eval(f().f_code, {'n': n-1, 'f': f}) * n).__code__, {'n': number, 'f': __import__('inspect').currentframe}))(int(input('请输入正整数：'))))

rabit = lambda n, a=1, b=1: rabit(n - 1, b, a + b) if n > 3 else a + b if n == 3 else 1
fact = lambda n, du=1: fact(n - du) * n if n else 1

def print99table():
    for a in range(1, 10):
        for b in range(1, a + 1):
            print(b, '*', a, '=', a*b, end='\n' if a == b else '\t')

    for i in range(45):
        print((a := int(sqrt(2 * i + .25) + .5)) and (b := i + 1 - a * (a - 1) // 2), '*', a, '=', a*b, end='\n' if a == b else '\t')

#from numpy import array
least = lambda X, Y: (b := ((X * Y).sum() - (vx := (sx := X.sum()) / (l := len(X))) * (sy := Y.sum())) / ((X**2).sum() - sx * vx), sy / l - b * vx)

def ls1(M,) -> float:
    M, l = iter(M), len(M) - 1
    return (sum(i * next(M) for i in range(-l, 2*l, 3)) / l + 2 * next(M)) / n * 2.

def LS(Y, X, n):
    _y, _x = sum(Y) / n, sum(X) / n
    _xy, _xx = _x * _y, _x * _x
    b = sum(Y[i] * X[i] - _xy for i in range(n)) / sum(X[i] ** 2  - _xx for i in range(n))
    return b, _y - b * _x

def ls(Y, n):
    sy, _x = sum(Y), (n - 1)
    b2 = 6 * (2 * sum(i * Y[i] for i in range(n)) - _x * sy) / ((n + 1) * n * _x)
    return b2, (sy / (n * 0.5) - b2 * _x) * 0.5

def ffsort(t: list, n: ('start', 'stop')=None) -> None:
    n, e, a = array('H', n or (0, len(t))), set(), 1

    while a:
        a = len(n) - 1
        for m in range(a):
            y = n[m]
            if y in e:
                a -= 1
            else:
                k = n[m + 1]
                if k - y < 10:
                    e.add(y)
                    for i in range(y, k):
                        while i > y and t[i] < t[i - 1]:
                            t[i], t[i - 1] = t[i - 1], t[i]
                            i -= 1
                else:
                    lev = sum(t[y : k]) / (k - y)
                    for i in range(y, k):
                        if t[i] > lev:
                            for u in range(i, k):
                                if t[u] < lev:
                                    t[i], t[u] = t[u], t[i]
                                    break
                            else:
                                n.insert(m + 1, i)
                                break


def o_sort(arr):
    for i in range(1, len(arr)):
        swp = arr[i]
        n = arr[i - 1]
        while i and n > swp:
            arr[i] = n
            i -= 1
            n = arr[i - 1]
        arr[i] = swp
    return arr

def sort(t: list) -> bool:
    x = False
    for i in range(1, len(t)):
        while i and t[i] < t[i - 1]:
            t[i], t[i - 1], x = t[i - 1], t[i], not x
            i -= 1
    return x

def reverse(o: tuple) -> bool:
    x, l = False, len(o)
    for i in range(l - 1):
        u = o[i]
        i += 1
        while i < l:
            if o[i] < u: x = not x
            i += 1
    return x

def _An(t: range, o=()) -> iter:
    if not t:
        yield o
        return
    for i in t:
        yield from _An(tuple(u for u in t if u != i), o + (i,))

def An(n: list, o=[]) -> iter:
    if not n:
        yield o
        return
    for i in range(len(n)):
        o.append(n.pop(i))
        yield from An(n)
        n.insert(i, o.pop())

def Mij(y, x, m: (tuple, range, range, len)):
    for i in m[1]:
        if i == y: continue
        i *= m[3]
        for u in m[2]:
            if u == x: continue
            yield m[0][i + u]

def det(r, n: int) -> int or float:
    c, a = 0, range(n)

    def _(t, o):
        nonlocal c
        if not t:
            d = 1 if sort(list(o)) else -1
            for i in a:
                d *= r[i * n + o[i]]
            c += d
            return
        for i in t:
            _(t - {i, }, o + (i,))

    _(set(a), ())
    return c

def inverse(t: tuple, n: len) -> array('f'):
    assert len(t) == n * n
    def _():
        if not f:
            d = -1 if reverse(o) else 1
            for i in a: d *= _M[i * n + o[i]]
            nonlocal u; u += d
            return
        for i in range(len(f)): o.append(f.pop(i)); _(); f.insert(i, o.pop())
    a = m = range(n)
    f, o, _M, u = list(a), [], t, 0
    _(); assert u   # if det(t) == 0, throw
    _det, n = u, f.pop()
    a, c, t = range(n), array('f'), (t, m, m, n)
    for x in m:
        for y in m: _M, u = tuple(Mij(y, x, t)), 0; _(); c.append((-u if x + y & 1 else u) / _det)
    return c

'''def _WLS(Y, X):
  n = len(X)
  WY, WX = array('f'), array('f')
  for i in range(n - 1):
    a = Y[i], X[i]
    u = i + 1
    x0, x1 = (Y[u] - a[0]) / u, (X[u] - a[1]) / u
    WY.append(a[0]); WX.append(a[1])
    for u in range(1, i): WY.append(x0 * u + a[0]); WX.append(a[1] + x1 * u)
  WY.append(Y[-1]), WX.append(X[-1])
  a = len(WX)
  _y, _x = sum(WY) / a, sum(WX) / a
  _xy, _xx = _x * _y, _x * _x
  a = sum(WY[i] * WX[i] - _xy for i in range(a)) / sum(WX[i] ** 2  - _xx for i in range(a))
  return a, _y - a * _x'''

def WLS(Y, X, W):
    ran = range(len(X))
    sw = sum(W)
    wy = sum(W[i] * Y[i] for i in ran)
    xw = sum(X[i] * W[i] for i in ran)
    b = xw / sw
    b = (sum(X[i] * W[i] * Y[i] for i in ran) - wy * b) /\
        (sum(X[i] ** 2   * W[i] for i in ran) - xw * b)
    return b, (wy - b * xw) / sw

#from numpy import array
wls = lambda Y, X, W: ((b := (((xw := X * W) * Y).sum() - ((sxw := xw.sum()) * (swy := (W * Y).sum())) / (sw := W.sum())) / ((xw * X).sum() - sxw ** 2 / sw)), (swy - b * sxw) / sw)

class uKFP:
    def __init__(s, *, _q, X=None, P=None):
        if not X: X = 0, 0
        if not P: P = 1, 0, 0, 1
        s._w = array('f', X + P + (_q, 0))

    def __call__(s, z, a=0.):
        w = s._w
        w[0] += w[1] + a * 0.5    # Xp
        w[1] += a
        w[3] += w[5]
        w[2] += w[3] + w[4] + w[6] # Pp
        w[4] += w[5]
        w[5] += w[6]
        a = 1. / (w[2] + 1.)   # r, if a close to -1, it may turn out mistakes
        w[7], a = w[2] * a, w[4] * a    # K
        z -= w[0]
        w[0] += w[7] * z    # X
        w[1] += a * z
        z = 1. - w[7]
        w[2] *= z
        w[3] *= z
        w[4] -= w[2] * a    # P
        w[5] -= w[3] * a
        return w

class KFP1(list):
    def __init__(self, *, _q, X=None, P=None):
        # if not X: self.X = np.mat([[0], [0]]).astype(np.float64)
        # elif not isinstance(X, np.matrix): self.X = np.mat(X)
        # else: self.X = X.astype(np.float64)
        # if not P: self.P = np.eye(2).astype(np.float64)
        # elif not isinstance(P, np.matrix): self.P = np.mat(P)
        # else: self.P = P.astype(np.float64)
        # self.I = np.eye(2, dtype=np.float64)
        # if np.isscalar(_q): self._q = _q * self.I
        # else: self._q = _q
        # self.H = np.mat([1, 0]).astype(np.float64)
        # self.r = np.mat([1.])
        # self.F = np.mat([1, 1, 0, 1]).astype(np.float64)
        super.__init__([0., 0.] if X is None else X)
        self.P = [1, 0, 0, 1] if P is None else P
        self._q = _q

    def __call__(self, z, a=0.):
        # xp = self.F * self.X + (a / 2., a)
        # pp = self.F * self.P * self.F.T + self._q
        # K = pp * self.H.T / (self.H * pp * self.H.T + self.r)
        # self.X = K * (z - (self.H * xp)) + xp
        # self.P = (self.I - K * self.H) * pp
        self[0] += self[1] + a * 0.5    # Xp
        self[1] += a
        self.P[0] = sum(self.P) + self._q # Pp
        self.P[1] += self.P[3]
        self.P[2] += self.P[3]
        self.P[3] += self._q
        a = 1. / (self.P[0] + 1)   # r, if a close to -1, it may turn out mistakes
        k, a = self.P[0] * a, self.P[2] * a    # K
        z -= self[0]
        self[0] += self._q * z    # X
        self[1] += a * z
        z = 1. - k
        self.P[0] *= z
        self.P[1] *= z
        self.P[2] -= self.P[0] * a    # P
        self.P[3] -= self.P[1] * a
        return self

class KFP:
    def __init__(self, dim_x, dim_z, dim_u=0):
        if dim_x < 1: raise ValueError
        if dim_z < 1: raise ValueError
        if dim_u < 0: raise ValueError
        self.dim_x = dim_x
        self.dim_z = dim_z
        self.dim_u = dim_u
        self.x = np.zeros((dim_x, 1), dtype=np.float64)
        self.P = np.eye(dim_x, dtype=np.float64)
        self.Q = np.eye(dim_x, dtype=np.float64)
        self.B = None
        self.F = np.eye(dim_x, dtype=np.float64)
        self.H = np.zeros((dim_z, dim_x), dtype=np.float64)
        self.R = np.eye(dim_z, dtype=np.float64)
        self.sq = 1.
        self.M = np.zeros((dim_x, dim_z), dtype=np.float64)
        self.z = np.array([None] * dim_z).T.astype(np.float64)
        self.I = np.eye(dim_z, dtype=np.float64)

    def predict(self, u=None, B=None, F=None, Q=None):
        if B is None: B = self.B
        if F is None: F = self.F
        if Q is None: Q = self.Q
        elif np.isscalar(Q):
            Q = np.eye(self.dim_x) * Q
        if B is None or u is None:
            self.x = np.dot(F, self.x)
        else:
            self.x = np.dot(F, self.x) + np.dot(B, u)
        self.P = self.sq * np.dot(np.dot(F, self.P), F.T) + Q

    def update(self, z, R=None, H=None):
        if z is None:
            self.z = np.array([None] * self.dim_z).T.astype(np.float64)
            self.y = np.zeros((self.dim_z, 1), dtype=np.float64)
            return
        if R is None: R = self.R
        elif np.isscalar(R): R = np.eye(self.dim_z, dtype=np.float64) * R
        if H is None:
            z = np.reshape(z, (self.dim_z, self.x.ndim))
            H = self.H
        self.y = z - np.dot(H, self.x)
        pht = np.dot(self.P, H.T)
        self.S = np.dot(self.P, pht) + R
        self.SI = np.invert(self.S)
        self.K = np.dot(pht, self.SI)
        self.x += np.dot(self.K, self.y)
        ikh = self.I - np.dot(self.K, H)
        self.P = np.dot(np.dot(ikh, self.P), ikh.T) + np.dot(np.dot(self.K, R), self.K.T)
        self.z = z


class GATE:
    from time import time
    def __init__(self, long, top=None):
        self.GT = self.SEP = 0
        self.T0 = self.time()
        self.OUTLINE = self.T1 = 0
        self.long = long
        self.top = top

    def iadd(self):
        self.GT += 1

    def __call__(self):
        T1 = self.time() - self.T0
        timeout = self.long * self.GT
        self.SEP = timeout - T1
        self.OUTLINE = timeout - self.T1
        if self.SEP < 0:
            self.OUTLINE -= self.SEP
            self.SEP = 0
        self.T1 = T1
        return self.SEP

    def __repr__(self):
        return f'Progress: {self.GT / self.top * 100 if self.top else self.GT:.2f}%; UsedTime: {self.T1:.2f}s; ' \
               f'OUTofSCUDLE: {self.OUTLINE:.2f}s; Budget: {self.timeout(self.top or self.GT) + self.OUTLINE:.2f}s.'

class N:
    def __init__(self, v, l=None, r=None):
        self.val, self.left, self.right = v, l, r
    def CountBinaryTreeTasksLeastUsedTime(root):
        def f(n):
            if not n: return 0, 0
            l, r = f(n.left), f(n.right)
            l, r, i = l[0], r[0], l[1] + r[1]
            return max(l, r, i) + n.val, i + n.val / 2# least time, total time
        return f(root)[0]

def canMakeSubsequence(str1, str2):
    l, li = len(str1), -1
    for x in str2:
        # u = 'z' if x == 'a' else chr(ord(x) - 1)
        for i in range(li + 1, l):
            if str1[i] == x: # or str[i] == u
                li = i
                break
        else: return False
    return True

def StepsOfSortThreeTupleArray(li):
    n = len(li)
    pass

def Func_LS(func, x0, x1, n):
    dx = x1 - x0
    sx = (x1 + x0) * 0.5
    ff = fxf = 0
    for x in range(x0, x1, dx / n):
        y = func(x)
        ff += y
        fxf += x * y
    a = (fxf - sx * ff) / ((x1 * x1 * x1 - x0 * x0 * x0) / 3 - sx * sx * dx)
    b = ff / dx - sx * a
    return a, b

def Func_LS(f, x0, x1, dx):
    assert x1 - x0 > dx > 0
    Ef, v = 0., 1. / (x1 - x0)
    u, b = 0., (x1 + x0) * 0.5
    while x0 < x1:
        Ef += (k := f(x0))
        u += x0 * k
        x0 += dx
    Ef *= (k := v * dx)
    u *= k
    k = 12. * (u - b * Ef) * (v * v)
    dx = Ef - k * b
    return lambda x: k * x + dx

def Reciprocal_LS(x0, x1):
    assert x1 > x0 > 0, ZeroDivisionError
    dx = x1 - x0
    sx = (x1 + x0) * 0.5
    ln = log(x1 / x0)
    a = (dx - sx * ln) / ((x1 * x1 * x1 - x0 * x0 * x0) / 3 - sx * sx * dx)
    b = ln / dx - sx * a
    return a, b

is_pow2 = lambda x: x > 0 and x ^ x - 1 == x | x - 1

def sigma(a):
    a = [i == '1' for i in a]
    k = 0
    f = 0
    w = False
    for i in range(len(a)):
        r = a[i]
        if r and not w:
            w = r
            k += 1
        elif not r and w:
            w = r
            f += 1

    print(f'duty {sum(a)/len(a)*100:.0f}%', 'h', k, 'l', f, 'freq', (k+f)/2/len(a)*60)

def show_Tk(fs=60):
    while 1:
        a = input('sigma')
        if not a or any(i not in '10_- ' for i in a): break
        a = [i == '1' for i in a if i in '10']
        k = 0
        f = 0
        w = False
        for i in range(len(a)):
            r = a[i]
            if r and not w:
                w = r
                k += 1
            elif not r and w:
                w = r
                f += 1

        print(f'duty {sum(a) / len(a) * 100:.0f}%', 'h', k, 'l', f, 'freq', (k + f) / 2 / len(a) * fs)

def LSFFT(data, sample_rate):
    import numpy as np
    from scipy.optimize import curve_fit
    n = len(data)
    t = np.arange(n) / sample_rate
    def model(t, *params):
        params = np.array(params)
        a = 2 * np.pi * params[1::3]
        a.resize((1, a.size))
        a = np.repeat(a, t.size, axis=0)
        t.resize((t.size, 1))
        result = (params[0::3] * np.sin(a * t + params[2::3])).sum(axis=1)
        t.resize(t.size)
        return result

    fft_results = np.fft.fft(data)
    print(fft_results.shape)
    fft_freqs = np.fft.fftfreq(n, d=1/sample_rate)
    ff = (0 <= fft_freqs) & (fft_freqs <= 200)
    sorted_indices = np.argsort(np.abs(fft_results))[::-1]
    sorted_indices = sorted_indices[ff[sorted_indices]][:n//3]  # Top 5 components
    fr = fft_results[sorted_indices]
    ft = fft_freqs[sorted_indices]
    initial_guess = np.empty(fr.size * 3)
    initial_guess[0::3] = np.abs(fr) / n * 2
    initial_guess[1::3] = ft
    initial_guess[2::3] = np.angle(fr)
    popt, _ = curve_fit(model, t, data, p0=initial_guess)
    print(popt)
    z = popt[0::3] * np.exp(1j * popt[2::3])
    freq = popt[1::3]
    d = freq.argsort()
    freq = freq[d]
    z = z[d]
    return z, freq
