import numpy as np
import matplotlib.pyplot as plt

# A short script to generate an image of two-dimensional, uniformly-
# distributed noise, illustrating "clustering".
# For more details, please see the blog article at:
# https://scipython.com/blog/poisson-disc-sampling-in-python/
# Christian Hill, March 2017.

width, height = 60, 45
N = width * height // 4
plt.scatter(np.random.uniform(0,width,N), np.random.uniform(0,height,N),
            c='g', alpha=0.6, lw=0)
plt.xlim(0,width)
plt.ylim(0,height)
plt.axis('off')
plt.savefig('uniform.png')
plt.show()
