"""Trainiert die Handschrift-Erkennung (Ziffern 0–9) neu und gibt den JS-Block DIGIT_NET aus.

Nur nötig, wenn die Erkennung verbessert werden soll (z. B. mit eigenen Kinder-Ziffern).
Voraussetzungen: pip install numpy scipy scikit-learn
MNIST (4 Dateien *-ubyte.gz) z. B. von https://github.com/fgnt/mnist in den Ordner werkzeuge/mnist/ legen.

Aufruf:  python werkzeuge/ziffern_trainieren.py  > werkzeuge/digitnet.js
Danach den Block `const DIGIT_NET = {...};` in src/App.jsx durch den neuen ersetzen.
Wichtig: Die Vorverarbeitung (normalize) muss zu recognizeDigit() in App.jsx passen
(Rahmen ausschneiden, längste Seite 20 px, nach Schwerpunkt in 28×28 zentrieren).
"""
import base64, gzip, os, sys
import numpy as np
from scipy import ndimage
from sklearn.neural_network import MLPClassifier

D = os.path.join(os.path.dirname(__file__), 'mnist')
rng = np.random.default_rng(1)


def imgs(f): return np.frombuffer(gzip.open(os.path.join(D, f)).read(), np.uint8, offset=16).reshape(-1, 28, 28)
def labs(f): return np.frombuffer(gzip.open(os.path.join(D, f)).read(), np.uint8, offset=8)


def normalize(img):
    a = img.astype(np.float32) / 255.
    ys, xs = np.nonzero(a > 0.1)
    if len(ys) == 0: return np.zeros((28, 28), np.float32)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = 20. / max(h, w)
    a = np.clip(ndimage.zoom(a, (max(1, round(h * s)) / h, max(1, round(w * s)) / w), order=1), 0, 1)
    out = np.zeros((28, 28), np.float32); h, w = a.shape
    oy, ox = (28 - h) // 2, (28 - w) // 2; out[oy:oy + h, ox:ox + w] = a
    cy, cx = ndimage.center_of_mass(out)
    return np.clip(ndimage.shift(out, (14 - cy, 14 - cx), order=1), 0, 1)


def augment(img):  # dicker/schräger geschrieben, wie Kinder mit dem Finger
    a = img.astype(np.float32)
    k = rng.integers(0, 3)
    if k: a = ndimage.grey_dilation(a, size=(k + 1, k + 1))
    a = ndimage.rotate(a, rng.uniform(-14, 14), reshape=False, order=1)
    sh = rng.uniform(-0.25, 0.25)
    a = ndimage.affine_transform(a, [[1, 0], [sh, 1]], offset=[0, -sh * 14], order=1)
    return np.clip(a * 1.6, 0, 255)


X, y = imgs('train-images-idx3-ubyte.gz'), labs('train-labels-idx1-ubyte.gz')
Xt, yt = imgs('t10k-images-idx3-ubyte.gz'), labs('t10k-labels-idx1-ubyte.gz')
Xtr = np.concatenate([np.array([normalize(x) for x in X]), np.array([normalize(augment(x)) for x in X])]).reshape(-1, 784)
ytr = np.concatenate([y, y])
clf = MLPClassifier(hidden_layer_sizes=(128,), alpha=1e-4, max_iter=25, batch_size=256, random_state=0).fit(Xtr, ytr)
print('// Testgenauigkeit:', clf.score(np.array([normalize(x) for x in Xt]).reshape(-1, 784), yt), file=sys.stderr)
W1, b1, W2, b2 = clf.coefs_[0], clf.intercepts_[0], clf.coefs_[1], clf.intercepts_[1]
q = lambda W: (np.round(W / (np.abs(W).max() / 127.)).astype(np.int8), float(np.abs(W).max() / 127.))
q1, s1 = q(W1); q2, s2 = q(W2)
enc = lambda a: base64.b64encode(a.astype(np.int8).tobytes()).decode()
print(f"""const DIGIT_NET = {{
  hidden: {W1.shape[1]},
  s1: {s1!r}, s2: {s2!r},
  w1: '{enc(q1.T)}',
  b1: {np.round(b1, 5).tolist()},
  w2: '{enc(q2.T)}',
  b2: {np.round(b2, 5).tolist()}
}};""")
