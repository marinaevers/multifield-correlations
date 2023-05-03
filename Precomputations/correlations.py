import os
import numpy as np
import netCDF4
import time

def correlations(DATA_PATH, SEGMENTATION_PATH, NUM_TIME_STEPS, SUBFOLDER = ""):
    # Compute total number of segments
    numSeg = 0
    numMembers = 0
    for field in os.listdir(DATA_PATH):
        if ".py" in field:
            continue
        if field in ["ts", "tas"]: # for these runs we only want to consider anomalies
            continue
        if numMembers == 0:
            if SUBFOLDER != "":
                field_path = os.path.join(os.path.join(DATA_PATH, field), SUBFOLDER)
            else:
                field_path = os.path.join(DATA_PATH, field)
            numMembers = len(os.listdir(field_path))
        seg = np.load(os.path.join(SEGMENTATION_PATH, field + ".npy"))
        numSeg += len(np.unique(seg))
    data = np.empty((numSeg, numMembers, NUM_TIME_STEPS))
    #corrs = np.empty((numSeg, numSeg, numMembers))
    filename = os.path.join(SEGMENTATION_PATH, "correlations.dat")
    corrs = np.memmap(filename, dtype='float32', mode='w+', shape=(numSeg, numSeg, numMembers))
    off = 0
    for field in sorted(os.listdir(DATA_PATH)):
        print(off)
        if ".py" in field:
            continue
        if field in ["ts", "tas"]: # for these runs we only want to consider anomalies
            continue
        # Load segmentation
        seg = np.load(os.path.join(SEGMENTATION_PATH, field+".npy"))
        # Average over segments, concatenate data
        if SUBFOLDER != "":
            field_path = os.path.join(os.path.join(DATA_PATH, field), SUBFOLDER)
        else:
            field_path = os.path.join(DATA_PATH, field)
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
            for i, s in enumerate(np.unique(seg)):
                data[i+off, j] = np.mean(timelines[seg == s], axis=0)
            ff.close()
        off += len(np.unique(seg))
    print("Loading done")
    for k in range(numMembers):
        print(k)
        start = time.time()
        print(data[:,k].shape)
        a = np.corrcoef(data[:,k])
        print(a.shape)
        print(corrs[:,:,k].shape)
        corrs[:,:,k] = a
        print(time.time()-start)
    corrs.flush()
    print("Writing done")
