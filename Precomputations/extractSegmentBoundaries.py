import os
import numpy as np
import alphashape
import json
import matplotlib.pyplot as plt


def computePointCloud(pixels):
    res = []
    for p in pixels:
        res.append([p[0]-0.5, p[1]-0.5])
        res.append([p[0]-0.5, p[1]+0.5])
        res.append([p[0]+0.5, p[1]-0.5])
        res.append([p[0]+0.5, p[1]+0.5])
        res.append([p[0], p[1]])
    return res
def computeSegmentHulls(f, PATH, roll):
    hulls = {}
    # Load segmentation
    print("Loading")
    print(f)
    segData = np.load(os.path.join(PATH, f+".npy"))
    if roll:
        segData = np.roll(segData, int(segData.shape[1]/2), axis=1)
    for i, s in enumerate(sorted(np.unique(segData))):
        # Create point cloud
        points = computePointCloud(np.argwhere(segData==s))
        hull = alphashape.alphashape(points, 1.9)
        try:
            hullT = np.array([hull.exterior.coords.xy[1], hull.exterior.coords.xy[0]]).T.tolist()
            hulls[i] = [hullT]
        except Exception as e:
            #print("No single hull")
            #print(len(hull.geoms))
            #print(s)
            #print(i)
            for h in hull.geoms:
                h = np.array([h.exterior.coords.xy[1], h.exterior.coords.xy[0]]).T.tolist()
                if not i in hulls:
                    hulls[i] =  [h]
                else:
                    hulls[i].append(h)
                #print(hulls[i])
    return hulls

def computeBoundaries(fields, PATH, roll = False):
    segmentHulls = {}
    for f in fields:
        segmentHulls[f] = computeSegmentHulls(f, PATH, roll)
    print("Computations done")
    json_object = json.dumps(segmentHulls)
    with open(os.path.join(PATH, "segmentPoints.json"), "w") as outfile:
        outfile.write(json_object)
    print("Writing done")

