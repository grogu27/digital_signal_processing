
import numpy as np
import matplotlib.pyplot as plt

# Исходные параметры
A = 4
f0 = 5
phi = np.pi / 6  # 30 градусов

T = 1 / f0
N = 1000

# Временная сетка: один период
t = np.linspace(0, T, N, endpoint=False)

# Гармонический сигнал
x = A * np.cos(2 * np.pi * f0 * t + phi)

# Численное вычисление коэффициентов
# Интегрирование методом прямоугольников
dt = T / N

a0 = 2 / T * np.sum(x) * dt

num_harmonics = 10

a = []
b = []

for n in range(1, num_harmonics + 1):
    an = 2 / T * np.sum(
        x * np.cos(2 * np.pi * n * f0 * t)
    ) * dt

    bn = 2 / T * np.sum(
        x * np.sin(2 * np.pi * n * f0 * t)
    ) * dt

    a.append(an)
    b.append(bn)

# Вывод результатов
print("a0 =", a0)

for n in range(num_harmonics):
    print(f"n={n+1}: a={a[n]:.5f}, b={b[n]:.5f}")

# График исходного сигнала
plt.figure(figsize=(10, 4))
plt.plot(t, x)
plt.title("Гармонический сигнал")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.grid()
plt.show()

# Спектр коэффициентов
plt.figure(figsize=(10, 4))
plt.stem(range(1, num_harmonics + 1), a)
plt.title("Коэффициенты an")
plt.xlabel("Номер гармоники")
plt.ylabel("Амплитуда")
plt.grid()
plt.show()

plt.figure(figsize=(10, 4))
plt.stem(range(1, num_harmonics + 1), b)
plt.title("Коэффициенты bn")
plt.xlabel("Номер гармоники")
plt.ylabel("Амплитуда")
plt.grid()
plt.show()
