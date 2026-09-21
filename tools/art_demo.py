"""D9 · ART 对抗样本演示（FGSM 对 sklearn 分类器）

用法：
    python art_demo.py
预期：对抗样本（eps=0.3）下准确率明显下降，说明模型鲁棒性不足。
"""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import SklearnClassifier

X, y = make_classification(n_samples=300, n_features=10, random_state=42)
# ART 的 SklearnClassifier 要求 one-hot 标签
enc = OneHotEncoder(sparse_output=False)
y_onehot = enc.fit_transform(y.reshape(-1, 1))

clf = SklearnClassifier(LogisticRegression())
clf.fit(X, y_onehot)
acc0 = (clf.predict(X).argmax(axis=1) == y).mean()
print(f"原始准确率      : {acc0:.3f}")

attack = FastGradientMethod(estimator=clf, eps=0.3)
X_adv = attack.generate(X)
acc1 = (clf.predict(X_adv).argmax(axis=1) == y).mean()
print(f"对抗样本准确率  : {acc1:.3f}（下降 {(acc0 - acc1):.3f}）")

# 不同扰动强度对比
for eps in [0.1, 0.3, 0.5, 1.0]:
    a = FastGradientMethod(estimator=clf, eps=eps)
    acc = (clf.predict(a.generate(X)).argmax(axis=1) == y).mean()
    print(f"  eps={eps:<4} -> 准确率 {acc:.3f}")
