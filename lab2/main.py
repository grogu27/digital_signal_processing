import numpy as np
import matplotlib.pyplot as plt



t = np.linspace(0 , 1 , 1000 )
A = 6
f = 5
#ph = np.pi / 2
#x = A * np.sin(2*np.pi*f*t + ph)
plt.figure(figsize=(10, 4))
i = 0
for A, ph in [(5, 0), (3, -np.pi/2), (2, np.pi/2)]:
    x =  A*np.sin(2*np.pi*f*t + ph)
    plt.subplot( 2 , 2 , i + 1)
    i+=1
    plt.plot(t, x, label=f"ph={ph:.2f}, A={A}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.axhline(0)
    plt.title( f"A={A}V, F={f} Hz, phi={ph:.2f} rad")

plt.savefig("signal.png", dpi=300)


#4
f = 5
T = 1/f
t2 = np.linspace(0, T*4, 1000)
x_t = 4 / np.pi * np.cos(2*np.pi * f * t2 - np.pi/2)
x2_t = 4 / (3*np.pi) * np.cos(2*np.pi * 3*f * t2 - np.pi/2)
x_sum_t = x_t + x2_t

plt.figure(figsize=(10, 4))
plt.plot(t2, x_sum_t, label="s(t)")
plt.plot(t2, x_t, label="x1(t)")
plt.plot(t2, x2_t, label="x2(t)")


plt.grid(True)
plt.xlabel("Time, s")
plt.ylabel("Amplitude, V")
plt.axhline(0)

plt.legend()
plt.savefig("sum_signal", dpi=300)

#5

f = 5
T = 1/f
k = [0, 1, 2, 3, 4, 5]
k2 = [1, 3, 5, 7, 9]

t2 = np.linspace(0, T*4, 1000)
x_sum_t = np.zeros_like(t2)
plt.figure(figsize=(10, 4))
n= 0
for i in k2:
    #x_sum_t += 4 / ((2*i-1) * np.pi) * np.cos(2*np.pi*(2*i-1)*f * t2 - np.pi/2)
    x_sum_t += 4 / (i * np.pi) * np.cos(2*np.pi*i*f * t2 - np.pi/2)

    plt.subplot( 2 , 3 , n + 1)
    n+=1
    plt.plot(t2, x_sum_t, label=f"s(t), k={n}")
    plt.grid(True)  
    plt.xlabel("Time, s")
    plt.ylabel("Amplitude, V")
    plt.legend()
    plt.axhline(0)

plt.savefig("meandr_signal", dpi=300)