import numpy as np
import matplotlib.pyplot as plt

A = 4
phi = np.pi / 4
k = 0.4
omega = k * np.pi
T = 2 * np.pi / omega
f_real = 1 / T

def func(t):
    return A * np.cos(omega * t + 0.25 * phi)

array_t = np.linspace(0, T*3+1, 10000)
x_t = []
buf = 0
for i in array_t:
    buf = func(i)
    x_t.append(buf)
#x_t = func(array_t)
array2_t = np.linspace(0, 1, 1000)
x2_t = 1 * np.sin(2 * np.pi * 2 * array2_t +   0.25 * 0)   
x3_t = 1/27 * np.sin(2 * np.pi * 27 * 2 * array2_t +   0.25 * 0)   
xsum_t = x2_t + x3_t




print(f"Период: {T}, Частота: {f_real}, Амплитуда: {A}, Fhi: {phi}, Omega: {omega}\nМаксимум для cos это 2*pi*k. Максимум: 0.4pi*t+0.25phi = 2pi*k, tmax = -(0.25phi/0.4pi)")
#print(x_t)

plt.figure(figsize=(10,4))
#plt.plot(array_t, x_t, color='red')
plt.plot(array2_t, xsum_t, color='green')
#plt.plot(array2_t, x3_t, color='black')

#plt.title(r'$x(t) = 4\cos(0.4\pi t + 0.25\varphi)$')
plt.title(f'x(t) = 4cos(0.4pi*t + 0.25phi)')
plt.axhline(0, color='black', linewidth=0.5)
#plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
#plt.axvline(T*3, color='black', linewidth=0.5, linestyle='--')


plt.xlabel('t, с')
plt.ylabel('x(t)')
plt.grid(True, alpha=0.3)
plt.savefig("signal.png", dpi=300, format='png')

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
# z1 = a + jb и z2 = a − jb
a1 = 5
a2 = 3
b1 = -1
b2 = 1
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