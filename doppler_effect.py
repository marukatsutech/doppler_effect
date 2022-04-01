# Doppler effect
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
import matplotlib.patches as patches


def update_observer():
    global position_a, position_b, y_at_wave0_a, y_at_wave0_b
    position_a = (x_a, y_a_init)
    position_b = (x_b, y_b_init)
    circle_a.set_center(position_a)
    y_at_wave0_a = a0 * np.sin(((k0 * x_a) - omega0 * cnt - phi0))
    line_a.set_data([x_a, x_a], [y_a_init, y_at_wave0_a])
    circle_b.set_center(position_b)
    y_at_wave0_b = a0 * np.sin(((k0 * x_b) - omega0 * cnt - phi0))
    line_b.set_data([x_b, x_b], [y_b_init, y_at_wave0_b])
    tx_a.set_position([x_a + 0.5, y_a_init])
    tx_b.set_position([x_b + 0.5, y_b_init])


def update_waves():
    global y0, wave0
    y0 = a0 * np.sin(((k0 * x) - omega0 * cnt - phi0))
    wave0.set_ydata(y0)
    pass


def change_v_b(value):
    global v_b
    v_b = float(value)
    update_waves()


def change_v_a(value):
    global v_a
    v_a = float(value)
    update_waves()


def change_phi0(value):
    global phi0
    phi0 = float(value)
    update_waves()


def change_omega0(value):
    global omega0
    omega0 = float(value)
    update_waves()


def change_k0(value):
    global k0
    k0 = float(value)
    update_waves()


def reset():
    global cnt, is_running, x_a, x_b
    cnt = 0
    is_running = False
    x_a = x_a_init
    x_b = x_a_init
    update_observer()


def switch():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True


def update(f):
    global cnt, x_a, x_b, position_a, position_b, tx_a, tx_b, line_a, y_at_wave0_a, line_b, y_at_wave0_b
    global y_observed_a, curve_observed_a, y_observed_b, curve_observed_b
    if is_running:
        tx_step.set_text(' Step(as t)=' + str(cnt))
        update_waves()
        x_a = x_a + v_a
        if x_a < x_min:
            x_a = x_max
        elif x_a > x_max:
            x_a = x_min
        else:
            pass
        x_b = x_b + v_b
        if x_b < x_min:
            x_b = x_max
        elif x_b > x_max:
            x_b = x_min
        else:
            pass
        update_observer()
        y_observed_a_roll = np.roll(y_observed_a, 1)
        y_observed_a = y_observed_a_roll
        y_observed_a[0] = y_at_wave0_a
        curve_observed_a.set_data(x, y_observed_a)
        y_observed_b_roll = np.roll(y_observed_b, 1)
        y_observed_b = y_observed_b_roll
        y_observed_b[0] = y_at_wave0_b
        curve_observed_b.set_data(x, y_observed_b)
        cnt += 1


# Global variables
is_running = False

x_min = -0.
x_max = 50.
y_min = -4.
y_max = 4.

cnt = 0

num_of_points = 500

a0_init = 1.
a0 = a0_init
k0_init = 1.
k0 = k0_init
omega0_init = 0.
omega0 = omega0_init
phi0_init = 0.
phi0 = phi0_init

x_a_init = x_max
x_a = x_a_init
y_a_init = -2.5
v_a_init = -0.1
v_a = v_a_init
x_b_init = x_max
x_b = x_a_init
y_b_init = -3.5
v_b_init = -0.1
v_b = v_b_init

# Generate figure and axes
fig = Figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

ax1.grid()
ax1.set_title('Doppler effect')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
ax1.set_aspect("equal")

ax2.grid()
# ax2.set_title('')
ax2.set_xlabel('Step/' + str(num_of_points))
ax2.set_ylabel('y at A')
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(y_min, y_max)
ax2.set_aspect("equal")

ax3.grid()
# ax3.set_title('')
ax3.set_xlabel('Step/' + str(num_of_points))
ax3.set_ylabel('y at B')
ax3.set_xlim(x_min, x_max)
ax3.set_ylim(y_min, y_max)
ax3.set_aspect("equal")

# Generate items
tx_step = ax1.text(x_min, y_max * 0.8, " Step(as t)=" + str(0))

x = np.linspace(0, x_max, num_of_points)
y0 = a0 * np.sin(((k0 * x) - omega0 * 0 - phi0))
wave0, = ax1.plot(x, y0, label='Wave0')
ax1.legend(prop={"size": 8}, loc="best")

position_a = [x_a, y_a_init]
circle_a = patches.Circle(xy=position_a, radius=0.3, color='blue')
ax1.add_patch(circle_a)
tx_a = ax1.text(x_a + 0.5, y_a_init, 'A')
y_at_wave0_a = a0 * np.sin(((k0 * x_a) - omega0 * 0 - phi0))
line_a, = ax1.plot([x_a, x_a], [y_a_init, y_at_wave0_a], color='blue')

position_b = [x_b, y_b_init]
circle_b = patches.Circle(xy=position_b, radius=0.3, color='red')
ax1.add_patch(circle_b)
tx_b = ax1.text(x_b + 0.5, y_b_init, 'B')
y_at_wave0_b = a0 * np.sin(((k0 * x_b) - omega0 * 0 - phi0))
line_b, = ax1.plot([x_b, x_b], [y_b_init, y_at_wave0_b], color='red')

y_observed_a = x * 0.
curve_observed_a, = ax2.plot(x, y_observed_a, color='blue')
y_observed_b = x * 0.
curve_observed_b, = ax3.plot(x, y_observed_b, color='red')

# Embed in Tkinter
root = tk.Tk()
root.title("Doppler effect")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

frm_w0 = ttk.Labelframe(root, relief="ridge", text="Wave0", labelanchor="n", width=100)
frm_w0.pack(side='left')
label_k0 = tk.Label(frm_w0, text="k0:")
label_k0.pack(side='left')
var_k0 = tk.StringVar(root)  # variable for spinbox-value
var_k0.set(k0_init)  # Initial value
s_k0 = tk.Spinbox(
    frm_w0, textvariable=var_k0, format="%.2f", from_=0.1, to=4., increment=0.01,
    command=lambda: change_k0(var_k0.get()), width=5
    )
s_k0.pack(side='left')
label_omega0 = tk.Label(frm_w0, text="Omega0:")
label_omega0.pack(side='left')
var_omega0 = tk.StringVar(root)  # variable for spinbox-value
var_omega0.set(omega0_init)  # Initial value
s_omega0 = tk.Spinbox(
    frm_w0, textvariable=var_omega0, format="%.2f", from_=-4., to=4., increment=0.01,
    command=lambda: change_omega0(var_omega0.get()), width=5
    )
s_omega0.pack(side='left')
label_phi0 = tk.Label(frm_w0, text="Phi0:")
label_phi0.pack(side='left')
var_phi0 = tk.StringVar(root)  # variable for spinbox-value
var_phi0.set(phi0_init)  # Initial value
s_phi0 = tk.Spinbox(
    frm_w0, textvariable=var_phi0, format="%.2f", from_=-2., to=10., increment=0.01,
    command=lambda: change_phi0(var_phi0.get()), width=5
    )
s_phi0.pack(side='left')

frm_v = ttk.Labelframe(root, relief="ridge", text="Velocity", labelanchor="n", width=100)
frm_v.pack(side='left')
label_v_a = tk.Label(frm_v, text="observer A:")
label_v_a.pack(side='left')
var_v_a = tk.StringVar(root)  # variable for spinbox-value
var_v_a.set(v_a_init)  # Initial value
s_v_a = tk.Spinbox(
    frm_v, textvariable=var_v_a, format="%.2f", from_=-1., to=1., increment=0.01,
    command=lambda: change_v_a(var_v_a.get()), width=5
    )
s_v_a.pack(side='left')
label_v_b = tk.Label(frm_v, text="observer B:")
label_v_b.pack(side='left')
var_v_b = tk.StringVar(root)  # variable for spinbox-value
var_v_b.set(v_b_init)  # Initial value
s_v_b = tk.Spinbox(
    frm_v, textvariable=var_v_b, format="%.2f", from_=-1., to=1., increment=0.01,
    command=lambda: change_v_b(var_v_b.get()), width=5
    )
s_v_b.pack(side='left')

btn = tk.Button(root, text="Play/Pause", command=switch)
btn.pack(side='left')

btn = tk.Button(root, text="Reset", command=reset)
btn.pack(side='left')

# main loop
anim = animation.FuncAnimation(fig, update, interval=200)
root.mainloop()
