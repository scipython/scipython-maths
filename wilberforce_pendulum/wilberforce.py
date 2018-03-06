import numpy as np
from scipy.integrate import odeint
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib

# Plot parameters related to the Wilberforce pendulum
# Mathematical details are available on my blog article,
# at https://scipython.com/blog/the-wilberforce-pendulum/
# Christian Hill, January 2016.

# Use LaTeX throughout the figure for consistency
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

# Parameters for the system
omega = 2.314       # rad.s-1
epsilon = 9.27e-3   # N
m = 0.4905          # kg
I = 1.39e-4         # kg.m2

def deriv(y, t, omega, epsilon, m, I):
    """Return the first derivatives of y = z, zdot, theta, thetadot."""
    z, zdot, theta, thetadot = y
    dzdt = zdot
    dzdotdt = -omega**2 * z - epsilon / 2 / m * theta
    dthetadt = thetadot
    dthetadotdt = -omega**2 * theta - epsilon / 2 / I * z
    return dzdt, dzdotdt, dthetadt, dthetadotdt

# The time grid in s
t = np.linspace(0,40,50000)
# Initial conditions: theta=2pi, z=zdot=thetadot=0
y0 = [0, 0, 2*np.pi, 0]

# Do the numerical integration of the equations of motion
y = odeint(deriv, y0, t, args=(omega, epsilon, m, I))
# Unpack z and theta as a function of time
z, theta = y[:,0], y[:,2]

# Plot z vs. t and theta vs. t on axes which share a time (x) axis
fig, ax_z = plt.subplots(1,1)
l_z, = ax_z.plot(t, z, 'g', label=r'$z$')
ax_z.set_xlabel('time /s')
ax_z.set_ylabel(r'$z /\mathrm{m}$', fontsize=18)
ax_theta = ax_z.twinx()
l_theta, = ax_theta.plot(t, theta, 'orange', label=r'$\theta$')
ax_theta.set_ylabel(r'$\theta /\mathrm{rad}$', fontsize=18)

# Add a single legend for the lines of both twinned axes
lines = (l_z, l_theta)
labels = [line.get_label() for line in lines]
plt.legend(lines, labels)
plt.savefig('wilberforce_z-t_plot.png')
plt.show()

# Plot theta vs. z on a cartesian plot
fig, ax1 = plt.subplots(1,1)
ax1.plot(z, theta, 'r', alpha=0.4)
ax1.set_xlabel(r'$z /\mathrm{m}$', fontsize=18)
ax1.set_ylabel(r'$\theta /\mathrm{rad}$', fontsize=18)
plt.savefig('wilberforce_theta-z_plot.png')
plt.show()

# Plot z vs. theta on a polar plot
fig, ax2 = plt.subplots(1,1, subplot_kw={'projection': 'polar'})
ax2.plot(theta, z, 'b', alpha=0.4)
plt.savefig('wilberforce_theta-z_polar_plot.png')
plt.show()
