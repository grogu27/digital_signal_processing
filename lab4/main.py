import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("figs", exist_ok=True)

# ============================================================
# Вспомогательные функции
# ============================================================

def rect_signal(t, tau, t0=0.0):
    return np.where((t >= t0) & (t < t0 + tau), 1.0, 0.0)


def fourier_numeric(t, x, freqs):
    trapz = getattr(np, "trapezoid", None) or np.trapz
    X = np.zeros(len(freqs), dtype=complex)
    for i, f in enumerate(freqs):
        integrand = x * np.exp(-1j * 2 * np.pi * f * t)
        X[i] = trapz(integrand, t)
    return X


def save_spectrum(freqs, X, title, path, tau_ref=None):
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(freqs, np.abs(X), 'b', lw=1.8)
    ax[0].set_ylabel('|X(f)|')
    ax[0].set_title(title + ' — модуль спектра')
    ax[0].grid(True)

    ax[1].plot(freqs, np.angle(X), 'r', lw=1.5)
    ax[1].set_ylabel('arg X(f), рад')
    ax[1].set_xlabel('f, Гц')
    ax[1].set_title('Аргумент спектра')
    ax[1].grid(True)

    if tau_ref is not None:
        for k in range(1, int(freqs[-1] * tau_ref) + 1):
            ax[0].axvline(k / tau_ref, color='gray', ls='--', lw=0.8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ============================================================
# Параметры
# ============================================================
tau = 2.0
f_max = 3.0 / tau
N = 4000
freqs = np.linspace(0, f_max, 600)

# ============================================================
# П.2
# ============================================================
print("=== П.2: ПФ прямоугольного сигнала ===")

t = np.linspace(-0.5 * tau, 1.5 * tau, N)
x = rect_signal(t, tau, t0=0.0)

f_check = [0.1 / tau, 0.5 / tau, 1.0 / tau]
X_check = fourier_numeric(t, x, np.array(f_check))
print("Проверка в точках:")
for f, val in zip(f_check, X_check):
    analytic = tau * np.sinc(f * tau) * np.exp(-1j * np.pi * f * tau)
    print(f"  f = {f:.4f} Гц: числ. = {val:.4f}, аналит. = {analytic:.4f}")

X = fourier_numeric(t, x, freqs)
save_spectrum(freqs, X, f'Прямоугольный сигнал, τ = {tau} c',
              'figs/p2_rect_spectrum.png', tau_ref=tau)

# ============================================================
# П.3
# ============================================================
print("\n=== П.3: Влияние длительности сигнала ===")

taus = [tau / 2, tau, tau * 2]
labels = [f'τ = {tt} c' for tt in taus]

fig, axes = plt.subplots(len(taus), 2, figsize=(12, 8), sharex=True)
for row, (tt, lab) in enumerate(zip(taus, labels)):
    t_loc = np.linspace(-0.5 * tt, 1.5 * tt, N)
    x_loc = rect_signal(t_loc, tt, t0=0.0)
    X_loc = fourier_numeric(t_loc, x_loc, freqs)

    axes[row, 0].plot(freqs, np.abs(X_loc), lw=1.8)
    axes[row, 0].set_ylabel(f'|X(f)|\n{lab}')
    axes[row, 0].grid(True)
    for k in range(1, int(freqs[-1] * tt) + 1):
        axes[row, 0].axvline(k / tt, color='gray', ls='--', lw=0.8)

    axes[row, 1].plot(freqs, np.angle(X_loc), 'r', lw=1.5)
    axes[row, 1].set_ylabel('arg X(f)')
    axes[row, 1].grid(True)

axes[0, 0].set_title('Модуль спектра')
axes[0, 1].set_title('Аргумент спектра')
axes[-1, 0].set_xlabel('f, Гц')
axes[-1, 1].set_xlabel('f, Гц')
fig.suptitle('П.3: Изменение длительности прямоугольного сигнала', fontsize=14)
fig.tight_layout()
fig.savefig('figs/p3_tau_variation.png', dpi=150)
plt.close(fig)

print("Вывод: при увеличении τ в 2 раза ширина главного лепестка |X(f)|")
print("уменьшается в 2 раза (нули смещаются к f = k/τ), а амплитуда растёт")
print("пропорционально τ. Аргумент меняется линейно с наклоном -π·τ.")

# ============================================================
# П.4
# ============================================================
print("\n=== П.4: Задержанный сигнал ===")

tau0 = tau / 2

t_d = np.linspace(-0.5 * tau, 2.5 * tau, N)
x_delayed = rect_signal(t_d, tau, t0=tau0)

X0 = fourier_numeric(t, x, freqs)
X_del = fourier_numeric(t_d, x_delayed, freqs)

fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharex=True)
axes[0, 0].plot(freqs, np.abs(X0), lw=1.8)
axes[0, 0].set_title('Модуль |X(f)| — исходный')
axes[0, 0].grid(True)
axes[0, 1].plot(freqs, np.angle(X0), 'r', lw=1.5)
axes[0, 1].set_title('Аргумент — исходный')
axes[0, 1].grid(True)

axes[1, 0].plot(freqs, np.abs(X_del), lw=1.8)
axes[1, 0].set_title(f'Модуль |X(f)| — задержанный на τ₀ = {tau0} c')
axes[1, 0].set_xlabel('f, Гц')
axes[1, 0].grid(True)
axes[1, 1].plot(freqs, np.angle(X_del), 'r', lw=1.5)
axes[1, 1].set_title('Аргумент — задержанный')
axes[1, 1].set_xlabel('f, Гц')
axes[1, 1].grid(True)
fig.suptitle('П.4: Свойство задержки сигнала', fontsize=14)
fig.tight_layout()
fig.savefig('figs/p4_delay.png', dpi=150)
plt.close(fig)

print("Вывод: задержка сигнала на τ₀ не меняет модуль спектра,")
print("но добавляет к аргументу линейный фазовый сдвиг -2π·f·τ₀.")

# ============================================================
# П.5
# ============================================================
print("\n=== П.5: Модуляция гармоническим колебанием ===")

f0 = 1.5 / tau
t_m = np.linspace(-0.5 * tau, 1.5 * tau, N)
x_rect = rect_signal(t_m, tau, t0=0.0)
carrier = np.cos(2 * np.pi * f0 * t_m)
x_mod = x_rect * carrier

X_rect = fourier_numeric(t_m, x_rect, freqs)
X_mod = fourier_numeric(t_m, x_mod, freqs)

fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharex=True)
axes[0, 0].plot(freqs, np.abs(X_rect), lw=1.8)
axes[0, 0].set_title('Модуль |X(f)| — прямоугольный импульс')
axes[0, 0].grid(True)
axes[0, 1].plot(freqs, np.angle(X_rect), 'r', lw=1.5)
axes[0, 1].set_title('Аргумент — прямоугольный импульс')
axes[0, 1].grid(True)

axes[1, 0].plot(freqs, np.abs(X_mod), lw=1.8)
axes[1, 0].set_title(f'Модуль |X(f)| — после умножения на cos(2π·{f0:.3f}·t)')
axes[1, 0].set_xlabel('f, Гц')
axes[1, 0].grid(True)
for k in range(1, int(freqs[-1] * tau) + 1):
    axes[1, 0].axvline(k / tau, color='gray', ls='--', lw=0.8)
axes[1, 1].plot(freqs, np.angle(X_mod), 'r', lw=1.5)
axes[1, 1].set_title('Аргумент — после модуляции')
axes[1, 1].set_xlabel('f, Гц')
axes[1, 1].grid(True)
fig.suptitle('П.5: Свойство модуляции (смещение спектра)', fontsize=14)
fig.tight_layout()
fig.savefig('figs/p5_modulation.png', dpi=150)
plt.close(fig)

print("Вывод: умножение импульса на гармоническое колебание частоты f₀")
print("приводит к смещению спектра: вместо одного лепестка около f = 0")
print("появляются два лепестка около f = ±f₀.")