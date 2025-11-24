import numpy as np
import bowyerWatsonTriag as bwt
import matplotlib.pyplot as plt

def getCircumcentre(vertices):
    v1,v2,v3 = vertices

def runVoroni(triangulation):
    circumcentres = []

    #iterate over the triangles to get their circum centres
    for t in triangulation:
        getCircumcentre(t.vertices)

if __name__ == '__main__':
    points = np.array([[3.0, 0.0], [2.0, 0.0], [2.0, 0.75],
                   [2.5, 0.75], [2.5, 0.6], [2.25, 0.6], 
                   [2.25, 0.2], [3.0, 0.2], [3.0, 0.0]])

    #an array of triangle objects
    triangulation = bwt.runBowyerWatson(points)
    runVoroni(triangulation)

