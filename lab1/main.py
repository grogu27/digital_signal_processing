import numpy as np
import matplotlib.pyplot as plt

A = 4
phi = np.pi / 4
omega = 0.4 * np.pi

T = 2 * np.pi / omega
f = 1 / T

def func(t, phi):
    return A * np.cos(omega * t + phi)

print("1. Параметры гармонического колебания")
print(f"Амплитуда: {A}")
print(f"Угловая частота: {omega:.4f} рад/с")
print(f"Период: {T:.2f} с")
print(f"Частота: {f:.2f} Гц")
print(f"Начальная фаза: {phi:.4f} рад")

delta_t = -phi / omega
print(f"Временной сдвиг: {delta_t:.4f} с")

t = np.linspace(0, 3 * T, 2000)
x1 = func(t, phi)
x0 = func(t, 0)

plt.figure(figsize=(10, 4))
plt.plot(t, x1, label="Начальная фаза π/4")
plt.plot(t, x0, "--", label="Начальная фаза 0")
plt.title("Гармонические колебания")
plt.xlabel("Время, с")
plt.ylabel("x(t)")
plt.axhline(0, color="black", linewidth=0.5)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("signal.png", dpi=300)
plt.close()

#plt.show()
time_points = [-1, 3, 7]
phase_deg = []
phase_rad = []
print("Общая формула: x(t)=Acos(wt+phi0), theta(t)=omega*t+0)\nT=5, w=2pi/T, w=2pi/5=0.4 rad/s\ntheta(t)=2pi*t/5")

for t in time_points:
    tmp = omega*t + phi
    phase_rad.append(tmp)
    #phase_deg.append(2*180*t/5)
    phase_deg.append(np.degrees(tmp))
    
phase_deg = [round(float(x), 2) for x in phase_deg]
phase_rad = [round(float(x), 4) for x in phase_rad]
print(f"Значение фазы колебания в моменты времени -1, 3, 7 сек: В градусах {phase_deg}, в радианах {phase_rad} ")


#   3
"""
# z1 = a + jb и z2 = a − jb
a1 = 5
a2 = 5
b1 = 1
b2 = -1
r1 = np.sqrt(a1**2 + b1**2)
r2 = np.sqrt(a2**2 + b2**2)
phi1 = np.arctan2(b1, a1)
phi2= np.arctan2(b2, a2)
print(f"Алгебраические формы комплексных числел: z1 = {a1} + j*{b1} и z2 = {a2} − j*{b2}")
print(f"Тригонометрические формы комплексных числел: z1 = {r1:.2f}*(cos{phi1:.2f} + i*sin{phi1:.2f})\nz2 = {r2:.2f}*(cos{phi2:.2f} + i*sin{phi2:.2f})")
print(f"Показательные формы комплексных числел: z1 = {r1:.2f}*e^(i*{phi1:.2f})\nz2 = {r2:.2f}*e^(i*{phi2:.2f})")

# 4

# z2 = 3.16*e^(i*0.32)
print("z2 = 3.16*e^(i*0.32) -> в алгебраическую форму:\n3.16*(cos(0.32) + i*sin(0.32))")
a3 = 3.16*np.cos(0.32)
b3 = 3.16*np.sin(0.32)
print(f"z2 = {a3:.0f} + i*{b3:.0f}")
"""

a1 = 5
a2 = 5
b1 = 1
b2 = -1
z1 = complex(a1, b1)
z2 = complex(a2, b2)

for name, z in [("z1", z1), ("z2", z2)]:
    r = abs(z)
    arg = np.angle(z)
    print(f"{name} = {z.real:g} + i*{z.imag:g}")
    print(
    f"Тригонометрическая форма: "
    f"{r:.4f}*(cos({arg:.4f}) "
    f"+ j*sin({arg:.4f}))"
    )
    print(f"Показательная форма: {r:.4f}*e^(j*{arg:.4f})")


# 4
r = abs(z1)
angle = np.arctan2(1, 3)
real_part = r * np.cos(angle)
im_part = r * np.sin(angle)
print(f"z = {r:.4f}*e^(j*{angle:.4f})")
print(f"z = {real_part:.4f} + i*{im_part:.4f}")