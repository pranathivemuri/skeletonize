import numpy as np
import time
from scipy import ndimage
from templateExpressions import us, ne, wd, es, uw, nd, sw, un, ed, nw, ue, sd


"""
   reference paper
   http://web.inf.u-szeged.hu/ipcg/publications/papers/PalagyiKuba_GMIP1999.pdf

"""
listOfalphas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def _getPaddedimage(image):
    """
       pads array in all dimension with 0s

    """

    zSize, ySize, xSize = np.shape(image)
    paddedShape = zSize + 2, ySize + 2, xSize + 2
    padImage = np.zeros((paddedShape), dtype=np.uint8)
    padImage[1:zSize + 1, 1:ySize + 1, 1:xSize + 1] = image
    return padImage


def _getBouondariesOfimage(image):
    """
       function to find boundaries/border/edges of the array/image

    """

    sElement = ndimage.generate_binary_structure(3, 1)
    erode_im = ndimage.morphology.binary_erosion(image, sElement)
    boundaryIm = image - erode_im
    assert np.sum(boundaryIm) <= np.sum(image)
    return boundaryIm

"""

each of the 12 iterations corresponds to each of the following
directions - us, ne, wd, es, uw, nd, sw, un, ed, nw, ue, sd
imported from template expressions
evaluated in advance using pyeda
https://pyeda.readthedocs.org/en/latest/expr.html

"""

directionList = [us, ne, wd, es,
                 uw, nd, sw, un,
                 ed, nw, ue, sd]


def _exceptionCurveEndpoint(validateMatrix):
    """

       if a voxel is a curve end point it has exactly voxel
       of value 1 in it's 26 connected neighbors, don't delete
       such voxels

    """
    if np.sum(validateMatrix) == 2:
        validate = False
    else:
        validate = True
    return validate


def _skeletonPass(image):
    """

        each pass consists of 12 serial subiterations and finding the
        boundaries of the padded image/array

    """
    numPixelsremoved = 0
    count = 0
    boundaryIm = _getBouondariesOfimage(image)
    numPixelsremovedList = []
    for direction in directionList:
        count += 1
        totalPixels, image = _applySubiter(image, boundaryIm, direction)
        numPixelsremovedList.append(totalPixels)
    numPixelsremoved = sum(numPixelsremovedList)
    return numPixelsremoved, image


def _applySubiter(image, boundaryIm, subiteration):
    """

       each subiteration paralleley reduces the border voxels in 12 directions
       going through each voxel and marking if it can be deleted or not in a
       different image named temp_del and finally multiply it with the original
       image to delete the voxels so marked

    """
    zPad, mPad, nPad = np.shape(image)
    nonZeropixels = np.sum(image)
    paddedShape = zPad, mPad, nPad
    temp_del = np.ones((paddedShape), dtype=np.uint8)
    numpixel_removed = 0

    for zdim in range(1, zPad - 1):
        for xdim in range(1, mPad - 1):
            for ydim in range(1, nPad - 1):
                if boundaryIm[zdim, xdim, ydim] == 1:
                    validateMatrix = image[zdim - 1: zdim + 2, xdim - 1: xdim + 2, ydim - 1: ydim + 2]
                    validateList = list(np.reshape(validateMatrix, 27))
                    del(validateList[13])
                    dictToBe = {}
                    for item in range(26):
                        dictToBe[listOfalphas[item]] = validateList[item]
                    delOrNot = eval(subiteration, dictToBe)
                    if np.uint8(delOrNot) == 1:
                        temp_del[zdim, xdim, ydim] = 0
                        numpixel_removed += 1
    image = np.multiply(image, temp_del)  # multiply the binary image with temp_del(image that marks edges as zeros)
    numpixel_removed = nonZeropixels - np.sum(image)
    return np.uint8(numpixel_removed), image


def getSkeletonize3D(image):
    """

    function to skeletonize a 3D binary image with object in brighter contrast than background.
    In other words, 1 = object, 0 = background

    """
    zOrig, yOrig, xOrig = np.shape(image)
    padImage = _getPaddedimage(image)
    start_skeleton = time.time()
    pass_no = 0
    numpixel_removed = 0
    while pass_no == 0 or numpixel_removed > 0:
        numpixel_removed, padImage = _skeletonPass(padImage)
        print("number of pixels removed in pass", pass_no, "is ", numpixel_removed)
        pass_no += 1
    print("done %i number of pixels in %i seconds" % (np.sum(image), time.time() - start_skeleton))
    return padImage[1: zOrig + 1, 1: yOrig + 1, 1: xOrig + 1]


if __name__ == '__main__':
    sample = np.ones((5, 5, 5), dtype=np.uint8)
    resultSkel = getSkeletonize3D(sample)
