# 3D Thinning using parallel 12 subiteration curve thinning by Palagyi
# http://web.inf.u-szeged.hu/ipcg/publications/papers/PalagyiKuba_GMIP1999.pdf
# using python
# need python > 3 to compile
# uses scipy, numpy and itertools packages
# uses mayavi for 3D visulization (compatible with python 2.7)
# palagyi3dthin.py is the heart of the algorithm
# template expressions.py are python evaluated boolean expressions
# thin3d templates.py is used to evaluate these expressions just once
# scratch folder conatains personal not so important different trials of 
# implementing the algorithm
# optimization folder contain memoizing, c code conversion to make the algorithm run
# faster, which are work in progress


