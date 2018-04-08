import numpy as np
import matplotlib.pyplot as plt
from poisson import PoissonDisc

# Generate periodogram images for uniformly-distributed noise and
# Poisson disc-sampled ("blue") noise in two dimensions.
# For mathematical details,  please see the blog articles at
# https://scipython.com/blog/poisson-disc-sampling-in-python/
# https://scipython.com/blog/power-spectra-for-blue-and-uniform-noise/
# Christian Hill, March 2017.

class UniformNoise():
    """A class for generating uniformly distributed, 2D noise."""

    def __init__(self, width=50, height=50, n=None):
        """Initialise the size of the domain and number of points to sample."""

        self.width, self.height = width, height
        if n is None:
            n = int(width * height)
        self.n = n

    def reset(self):
        pass

    def sample(self):
        return np.array([np.random.uniform(0, width, size=self.n),
                         np.random.uniform(0, height, size=self.n)]).T

# domain size, minimum distance between samples for Poisson disc method...
width = height = 100
r = 2
poisson_disc = PoissonDisc(width, height, r)
# Expected number of samples from Poisson disc method...
n = int(width * height / np.pi / poisson_disc.a**2)
# ... use the same for uniform noise.
uniform_noise = UniformNoise(width, height, n)

# Number of sampling runs to do (to remove noise from the noise in the power
# spectrum).
N = 100
# Sampling parameter, when putting the sample points onto the domain
M = 5

fig, ax = plt.subplots(nrows=2, ncols=2)

for j, noise in enumerate((poisson_disc, uniform_noise)):
    print(noise.__class__.__name__)
    spec = np.zeros((height * M, width * M))
    for i in range(N):
        print('{}/{}'.format(i+1, N))
        noise.reset()
        samples = np.array(noise.sample())
        domain = np.zeros((height * M, width * M))
        for pt in samples:
            coords = int(pt[1] * M), int(pt[0] * M)
            domain[coords] = 1

        # Do the Fourier Trasform, shift the frequencies and add to the
        # running total.
        f = np.fft.fft2(domain)
        fshift = np.fft.fftshift(f)
        spec += np.log(np.abs(fshift))
    
    # Plot the a set of random points and the power spectrum.
    ax[0][j].imshow(domain, cmap=plt.cm.Greys)
    ax[1][j].imshow(spec, cmap=plt.cm.Greys_r)
    # Remove axis ticks and annotations
    for k in (0,1):
        ax[k][j].tick_params(which='both', bottom='off', left='off',
                top='off', right='off', labelbottom='off', labelleft='off')

plt.savefig('periodograms.png')
plt.show()
