import numpy as np
import matplotlib.pyplot as plt

A = 4
phi = 0
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
x2_t = A * np.cos(k * np.pi * array_t -  0.25 * 360)   
x3_t = A * np.cos(k * np.pi * array_t +  0.25 * phi)   


print(f"Период: {T}, Частота: {f_real}, Амплитуда: {A}, Fhi: {phi}, Omega: {omega}\nМаксимум для cos это 2*pi*k. Максимум: 0.4pi*t+0.25phi = 2pi*k, tmax = -(0.25phi/0.4pi)")
#print(x_t)

plt.figure(figsize=(10,4))
plt.plot(array_t, x_t, color='red')
#plt.plot(array_t, x2_t, color='green')
#plt.plot(array_t, x3_t, color='black')

#plt.title(r'$x(t) = 4\cos(0.4\pi t + 0.25\varphi)$')
plt.title(f'x(t) = 4cos(0.4pi*t + 0.25phi)')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(T*3, color='black', linewidth=0.5, linestyle='--')


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
print(f"Значение фазы колебания в моменты времени -1, 3, 7 сек: В градусах {phase_deg}, в радианах {phase_rad}, ")