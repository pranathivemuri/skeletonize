from scipy.misc import imread
import numpy as np

import time
import os

from Palagy3dthin import getSkeletonize3D

"""takes in 2D image slices from the root directory
    converts them to binary and returns the thinnned 3d volume
"""

from skimage.filters import threshold_otsu


def convertToBinary(image, convert):
    """
    threshod an image and display, a global threshold image is in binary_global if convert is True,
    object is in brighter contrast and viceversa
    """
    global_thresh = threshold_otsu(image)
    if convert:
        binary_global = image > global_thresh
    else:
        binary_global = image < global_thresh
    return np.uint8(binary_global), global_thresh


if __name__ == '__main__':
    startt = time.time()
    count = 0
    root = "/Users/3scan_editing/Desktop/twodimageslices"
    for file in os.listdir(root):
        if file.endswith(".jpg"):
            count = count + 1
    i = imread((os.path.join(root, file)))
    m, n = np.shape(i)
    inputIm = np.zeros((count, m, n), dtype=np.uint8)
    count1 = 0
    print("x, y, z dimensions are %i %i %i  " % (m, n, count))
    dimensions = (m, n, count)
    globalThresholdsList = []
    for file in os.listdir(root):
        if file.endswith(".jpg"):
            i = imread((os.path.join(root, file)))
            # thresholdedIm, globalThreshold = convertToBinary(i, False)
            # globalThresholdsList.append(globalThreshold)
            inputIm[count1][:][:] = i
            count1 += 1
    thresholdedIm, globalThreshold = convertToBinary(inputIm, False)
    print("skeletonizing started at", startt)
    print("threshold of the 3d volume is", globalThreshold)
    np.save('/Users/3scan_editing/thinning/input3dtest.npy', thresholdedIm)
    skeletonIm = getSkeletonize3D(thresholdedIm)
    np.save('/Users/3scan_editing/thinning/skeleton3dtest.npy', skeletonIm)
    print("skeletonizing ended at", time.time())
    print("time taken to skeletonize the %i image is %i" % (dimensions, (time.time() - startt)))
    # mlab.contour3d(skeletonStackAlloc)
