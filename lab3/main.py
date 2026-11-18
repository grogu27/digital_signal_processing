import numpy as np
import matplotlib.pyplot as plt
import os

if not os.path.exists("plots"):
    os.makedirs("plots")

_trapz = getattr(np, "trapezoid", None) or np.trapz

# Порог отсечения численного шума по АМПЛИТУДЕ.
# Для метода трапеций с ~10^4 точками остатки интеграла обычно ~1e-5..1e-4.
THRESHOLD = 1e-3

# Порог для отдельных коэффициентов a_n, b_n.
# Если |a_n| или |b_n| меньше этого значения — считаем коэффициент нулём.
COEF_EPS = 1e-6


def compute_phases(a, b, harmonics, threshold=THRESHOLD, coef_eps=COEF_EPS):
    """
    Возвращает (amplitude_spectrum, phase_spectrum, valid_mask)
    для гармоник n = 1..harmonics.

    Логика:
      - Если A_n < threshold          -> фаза = 0 (шум)
      - Если |b_n| < coef_eps          -> чистый косинус: фаза = 0 (если a_n>0)
      - Если |a_n| < coef_eps          -> чистый синус: фаза = -pi/2 (если b_n>0)
      - Иначе                          -> честный arctan2(-b_n, a_n)
    """
    amp = np.hypot(a[1:harmonics + 1], b[1:harmonics + 1])
    phase = np.zeros(harmonics)

    for i in range(harmonics):
        n = i + 1
        if amp[i] < threshold:
            phase[i] = 0.0
            continue

        an, bn = a[n], b[n]

        if abs(bn) < coef_eps:
            # Чистый косинус (или его отсутствие)
            phase[i] = 0.0 if an >= 0 else np.pi
        elif abs(an) < coef_eps:
            # Чистый синус
            phase[i] = -np.pi / 2 if bn > 0 else np.pi / 2
        else:
            phase[i] = np.arctan2(-bn, an)

    valid_mask = amp > threshold
    return amp, phase, valid_mask


# ------------------------------------------------------------
# 1. Ряд Фурье гармонического колебания
# ------------------------------------------------------------
def harmonic_fourier(amplitude=2.0, frequency=5.0, phase=0.0,
                     harmonics=4, samples=10000):
    period = 1.0 / frequency
    t = np.linspace(0.0, period, samples, endpoint=False)
    x = amplitude * np.cos(2 * np.pi * frequency * t + phase)

    a = np.zeros(harmonics + 1)
    b = np.zeros(harmonics + 1)

    a[0] = (1.0 / period) * _trapz(x, t)
    for n in range(1, harmonics + 1):
        a[n] = (2.0 / period) * _trapz(
            x * np.cos(2 * np.pi * n * frequency * t), t)
        b[n] = (2.0 / period) * _trapz(
            x * np.sin(2 * np.pi * n * frequency * t), t)

    amplitude_spectrum, phase_spectrum, valid_mask = compute_phases(
        a, b, harmonics)

    print("\n1. ГАРМОНИЧЕСКОЕ КОЛЕБАНИЕ")
    print(f"A = {amplitude}, f0 = {frequency} Гц, phase = {phase:.4f} рад")
    print(" n          an              bn              An          phi(n)")
    for n in range(harmonics + 1):
        An = np.hypot(a[n], b[n]) if n > 0 else abs(a[0])
        if n == 0:
            phin = 0.0
        elif An < THRESHOLD:
            phin = 0.0
        else:
            _, phin, _ = compute_phases(a, b, n)
            phin = phin[-1]
        print(f"{n:2d}  {a[n]:14.8f}  {b[n]:14.8f}  "
              f"{An:12.8f}  {phin:12.8f}")

    n_values = np.arange(1, harmonics + 1)
    fig, axes = plt.subplots(3, 1, figsize=(9, 9))

    axes[0].plot(t, x)
    axes[0].set_title(f"x(t)=A·cos(2πf₀t+φ), φ={phase:.3f}")
    axes[0].set_xlabel("t, с"); axes[0].set_ylabel("x(t)"); axes[0].grid(True)

    # Амплитуды — только значимые (шум не рисуем)
    axes[1].stem(n_values[valid_mask], amplitude_spectrum[valid_mask])
    axes[1].set_title("Амплитудный спектр Aₙ")
    axes[1].set_xlabel("n"); axes[1].grid(True)
    axes[1].set_xticks(n_values)

    # Фазы — рисуем ВСЕ гармоники, шумовые уже занулены в phase_spectrum.
    # Так видно, что "шумовых" фаз нет — они ровно 0.
    axes[2].stem(n_values, phase_spectrum)
    axes[2].set_title("Фазовый спектр φ(n)")
    axes[2].set_xlabel("n"); axes[2].set_ylabel("рад"); axes[2].grid(True)
    axes[2].set_xticks(n_values)
    axes[2].set_ylim(-np.pi - 0.2, np.pi + 0.2)

    plt.tight_layout()
    filename = f"plots/1_harmonic_phase_{phase:.2f}.png".replace('.', '_', 1)
    plt.savefig(filename, dpi=150)
    plt.close(fig)


# ------------------------------------------------------------
# 2. Прямоугольный сигнал: коэффициенты и синтез
# ------------------------------------------------------------
def rectangular_fourier(period=0.1, pulse_width=0.05, amplitude=1.0,
                        max_harmonic=6, samples=20000):
    if not (0 < pulse_width <= period):
        raise ValueError("0 < τ ≤ T")

    t = np.linspace(0.0, period, samples, endpoint=False)
    x = np.where(t < pulse_width, amplitude, 0.0)

    a0 = (1.0 / period) * _trapz(x, t)
    a = np.zeros(max_harmonic + 1)
    b = np.zeros(max_harmonic + 1)
    for n in range(1, max_harmonic + 1):
        ang = 2 * np.pi * n * t / period
        a[n] = (2.0 / period) * _trapz(x * np.cos(ang), t)
        b[n] = (2.0 / period) * _trapz(x * np.sin(ang), t)

    An, phin, valid_mask = compute_phases(a, b, max_harmonic)

    print("\n2. ПРЯМОУГОЛЬНЫЙ СИГНАЛ")
    print(f"T={period} с, τ={pulse_width} с, A={amplitude}, "
          f"Q=T/τ={period/pulse_width:.2f}")
    print(f"a0 = {a0:.8f}")
    print(" n          an              bn              An          phi(n)")
    for n in range(1, max_harmonic + 1):
        print(f"{n:2d}  {a[n]:14.8f}  {b[n]:14.8f}  "
              f"{An[n-1]:12.8f}  {phin[n-1]:12.8f}")

    t_many = np.linspace(0.0, 3 * period, 3 * samples, endpoint=False)
    x_many = np.where(np.mod(t_many, period) < pulse_width, amplitude, 0.0)

    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    axes[0].plot(t_many, x_many); axes[0].grid(True)
    axes[0].set_title("Периодический прямоугольный сигнал")
    axes[0].set_xlabel("t, с")

    nv = np.arange(1, max_harmonic + 1)
    axes[1].stem(nv[valid_mask], An[valid_mask])
    axes[1].set_title("Спектр амплитуд (до 6-й)")
    axes[1].set_xlabel("n"); axes[1].grid(True); axes[1].set_xticks(nv)

    axes[2].stem(nv, phin)
    axes[2].set_title("Спектр фаз (до 6-й)")
    axes[2].set_xlabel("n"); axes[2].set_ylabel("рад"); axes[2].grid(True)
    axes[2].set_xticks(nv)
    axes[2].set_ylim(-np.pi - 0.2, np.pi + 0.2)

    plt.tight_layout()
    filename = f"plots/2_rect_T_{period}_tau_{pulse_width}.png".replace('.', '_', 1)
    plt.savefig(filename, dpi=150)
    plt.close(fig)

    # Синтез по 2, 4, 6 гармоникам
    t_s = np.linspace(0.0, 3 * period, 3000, endpoint=False)
    x_orig = np.where(np.mod(t_s, period) < pulse_width, amplitude, 0.0)

    fig2 = plt.figure(figsize=(10, 5))
    plt.plot(t_s, x_orig, "k", lw=2, label="исходный")
    for count in (2, 4, 6):
        xs = np.full_like(t_s, a0)
        for n in range(1, count + 1):
            ang = 2 * np.pi * n * t_s / period
            xs += a[n] * np.cos(ang) + b[n] * np.sin(ang)
        plt.plot(t_s, xs, label=f"{count} гармоник")
    plt.title(f"Синтез: T={period}, τ={pulse_width}")
    plt.xlabel("t, с"); plt.ylabel("x"); plt.grid(True); plt.legend()
    plt.tight_layout()

    filename2 = f"plots/2_synth_T_{period}_tau_{pulse_width}.png".replace('.', '_', 1)
    plt.savefig(filename2, dpi=150)
    plt.close(fig2)


# ------------------------------------------------------------
# 3. Проверка ортогональности
# ------------------------------------------------------------
def orthogonality_check(period=1.0, max_n=10, samples=20000):
    t = np.linspace(0.0, period, samples, endpoint=False)
    dt = period / samples
    f1 = 1.0 / period

    print("\n3a. ОРТОГОНАЛЬНОСТЬ sin(kωt) и sin(nωt)")
    print("     (должно быть 0 вне диагонали k=n)")
    for k in range(1, max_n + 1):
        row = []
        sk = np.sin(2 * np.pi * k * f1 * t)
        for n in range(1, max_n + 1):
            sn = np.sin(2 * np.pi * n * f1 * t)
            row.append(np.sum(sk * sn) * dt)
        print(f"k={k:2d}: " + " ".join(f"{v: .3f}" for v in row))

    print("\n3b. ОРТОГОНАЛЬНОСТЬ e^{jkωt} и e^{jnωt} (с сопряжением)")
    print("     (должно быть T на диагонали k=n, 0 иначе)")
    for k in range(-max_n, max_n + 1):
        row = []
        sk = np.exp(1j * 2 * np.pi * k * f1 * t)
        for n in range(-max_n, max_n + 1):
            sn = np.exp(1j * 2 * np.pi * n * f1 * t)
            integral = np.sum(sk * np.conj(sn)) * dt
            row.append(integral.real)
        print(f"k={k:3d}: " + " ".join(f"{v: .2f}" for v in row))

    print("\n3c. Нарушение при изменении частоты второго сигнала")
    k, n = 1, 2
    sk = np.sin(2 * np.pi * k * f1 * t)
    for factor in (1.0, 1.3, 2.0):
        sn = np.sin(2 * np.pi * n * f1 * factor * t)
        val = np.sum(sk * sn) * dt
        print(f"  f2 = {factor}·f₁·n  →  ∫ = {val: .6f}")

    print("\n3d. Интеграл на разных интервалах (k=1, n=2)")
    sn = np.sin(2 * np.pi * n * f1 * t)
    for frac in (1.0, 0.5, 0.25):
        mask = t < frac * period
        val = np.sum(sk[mask] * sn[mask]) * dt
        print(f"  интервал 0..{frac}·T  →  ∫ = {val: .6f}")


if __name__ == "__main__":
    harmonic_fourier(2.0, 5.0, 0.0)
    harmonic_fourier(2.0, 5.0, np.pi / 4)

    rectangular_fourier(0.1, 0.05)
    rectangular_fourier(0.1, 0.025)
    rectangular_fourier(0.2, 0.05)

    orthogonality_check(1.0, 10)

    print("\nВсе графики сохранены в папку 'plots'.")