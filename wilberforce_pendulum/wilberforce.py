import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib

# Plot parameters related to the Wilberforce pendulum
# Mathematical details are available on my blog article,
# at https://scipython.com/blog/the-wilberforce-pendulum/
# Christian Hill, January 2016.
# Updated (January 2020) to use solve_ivp instead of odeint.

# Use LaTeX throughout the figure for consistency.
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

# Parameters for the system
omega = 2.314       # rad.s-1
epsilon = 9.27e-3   # N
m = 0.4905          # kg
I = 1.39e-4         # kg.m2

def deriv(t, y, omega, epsilon, m, I):
    """Return the first derivatives of y = z, zdot, theta, thetadot."""
    z, zdot, theta, thetadot = y
    dzdt = zdot
    dzdotdt = -omega**2 * z - epsilon / 2 / m * theta
    dthetadt = thetadot
    dthetadotdt = -omega**2 * theta - epsilon / 2 / I * z
    return dzdt, dzdotdt, dthetadt, dthetadotdt

# Initial conditions: theta=2pi, z=zdot=thetadot=0
y0 = [0, 0, 2*np.pi, 0]

# Do the numerical integration of the equations of motion up to tmax secs.
tmax = 40
soln = solve_ivp(deriv, (0, tmax), y0, args=(omega, epsilon, m, I), dense_output=True)
# The time grid in s
t = np.linspace(0, tmax, 2000)
# Unpack z and theta as a function of time
z, theta = soln.sol(t)[0], soln.sol(t)[2]

# Plot z vs. t and theta vs. t on axes which share a time (x) axis
fig, ax_z = plt.subplots()
l_z, = ax_z.plot(t, z, 'g', label=r'$z$')
ax_z.set_xlabel('time /s')
ax_z.set_ylabel(r'$z /\mathrm{m}$')
ax_theta = ax_z.twinx()
l_theta, = ax_theta.plot(t, theta, 'orange', label=r'$\theta$')
ax_theta.set_ylabel(r'$\theta /\mathrm{rad}$')

# Add a single legend for the lines of both twinned axes
lines = (l_z, l_theta)
labels = [line.get_label() for line in lines]
plt.legend(lines, labels)
plt.tight_layout()
plt.savefig('wilberforce_z-t_plot.png')
plt.show()

# Plot theta vs. z on a cartesian plot
fig, ax1 = plt.subplots()
ax1.plot(z, theta, 'r', alpha=0.8)
ax1.set_xlabel(r'$z /\mathrm{m}$')
ax1.set_ylabel(r'$\theta /\mathrm{rad}$')
plt.tight_layout()
plt.savefig('wilberforce_theta-z_plot.png')
plt.show()

# Plot z vs. theta on a polar plot
fig, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
ax2.plot(theta, z, 'b', alpha=0.8)
plt.tight_layout()
plt.savefig('wilberforce_theta-z_polar_plot.png')
plt.show()
