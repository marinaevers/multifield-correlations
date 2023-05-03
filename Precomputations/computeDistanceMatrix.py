import numpy as np
import os
import netCDF4
from helper.pearson import pearson_corr_distance_matrix
import time as t


def computeDistanceMatrix(DATA_PATH, SEGMENTATION_PATH, OUT_PATH, NUM_TIME_STEPS, SUBFOLDER = ""):
    print("Distances")
    print(os.path.join(OUT_PATH, 'distances.npy'))
    timeSeries = {}
    dataAllFields = np.empty((0, 0))
    for field in sorted(os.listdir(DATA_PATH)):
        if ".py" in field:
            continue
        print(field)
        if field in ["ts", "tas"]: # for these runs we only want to consider anomalies
            continue
        # Load segmentation
        seg = np.load(os.path.join(SEGMENTATION_PATH, field+".npy"))
        # Average over segments, concatenate data
        if SUBFOLDER != "":
            field_path = os.path.join(os.path.join(DATA_PATH, field), SUBFOLDER)
        else:
            field_path = os.path.join(DATA_PATH, field)
        data = np.empty((0, 0))
        for j, run in enumerate(sorted(os.listdir(field_path))):
            path = os.path.join(field_path, run)
            ff = netCDF4.Dataset(path)
            variable = field
            if "Anomaly" in field:
                variable = field[:-7]
            if "pr" in variable:
                variable = "pr"
            timelines = ff.variables[variable]
            timelines = np.transpose(timelines, axes=[1, 2, 0])
            # Average over segments
            tAv = np.empty((len(np.unique(seg)),NUM_TIME_STEPS))
            for i, s in enumerate(sorted(np.unique(seg))):
                tAv[i] = np.mean(timelines[seg == s], axis=0)
            if(data.shape == (0,0)):
                data = tAv
            else:
                data = np.append(data, tAv, axis=1)
            ff.close()
        # Normalize data
        if dataAllFields.shape == (0,0):
            dataAllFields = data
        else:
            dataAllFields = np.append(dataAllFields, data, axis=0)
        print(field + " done")
        print(dataAllFields.shape)

    # Compute pair-wise correlations (among all fields)
    start_time = t.time()
    distance_matrix = pearson_corr_distance_matrix(timelines=dataAllFields, lag=0)
    distance_matrix = -(distance_matrix+1)*0.5+1
    np.save(os.path.join(OUT_PATH, 'distances.npy'), distance_matrix)
    print(distance_matrix.shape)

    print('... calculated full correlation in %s seconds' % (t.time() - start_time))
