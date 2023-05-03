import numpy as np
import utils as u
import matplotlib.pyplot as plt
import os



def createImage(MDS_POINTS_PATH, SHAPE):
    for f in os.listdir(MDS_POINTS_PATH):
        print(f)
        if not ".npy" in f or not "y_full" in f:
            continue
        path = os.path.join(MDS_POINTS_PATH, f)
        mds_points = np.load(path)
        name = f[7:-4]
        plt.imsave(os.path.join(MDS_POINTS_PATH, name + ".png"), u.mds_image(mds_points, SHAPE)[::-1])
