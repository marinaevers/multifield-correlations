import json
import os
import numpy as np
import netCDF4
import statsmodels.api as sm
import matplotlib.pyplot as plt

def segmentMedian(DATA_PATH, SEGMENTATION_PATH, NUM_TIME_STEPS, SUBFOLDER = "", outOfCore=True, numMembers = 100):
    timeSeries = {}
    numFields = 0
    fieldMap = {}
    for field in sorted(os.listdir(DATA_PATH)):
        if ".py" in field:
            continue
        if field in ["ts", "tas"]: # for these runs we only want to consider anomalies
            continue
        fieldMap[field] = numFields
        numFields += 1
    for field in sorted(os.listdir(DATA_PATH)):
        if ".py" in field:
            continue
        filename = os.path.join(SEGMENTATION_PATH, field+"AllSeries.dat")
        # Load segmentation
        seg = np.load(os.path.join(SEGMENTATION_PATH, field+".npy"))
        allSeries = np.memmap(filename, dtype='float32', mode='w+', shape=(len(np.unique(seg)), numMembers, NUM_TIME_STEPS))
        if ".py" in field:
            continue
        if field in ["ts", "tas"]: # for these runs we only want to consider anomalies
            continue
        timeSeries[field] = {}
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
                data = np.append(data, tAv, axis=0)
            ff.close()
        numSeg = len(np.unique(seg))
        for i, s in enumerate(sorted(np.unique(seg))):
            minSeries = np.min(data[i::numSeg], axis=0)
            maxSeries = np.max(data[i::numSeg], axis=0)
            try:
                fig, depth, ix_depth, ix_outliers = sm.graphics.fboxplot(data[i::numSeg])
                plt.close(fig)
                medianSeries = data[i::numSeg][ix_depth[0]].tolist()
            except:
                medianSeries = np.mean(data[i::numSeg], axis=0).tolist()
            timeSeries[field][i] = [list(medianSeries), list(minSeries), list(maxSeries)]
            allSeries[i] = data[i::numSeg].tolist()

        json_object = json.dumps(timeSeries)
        allSeries.flush()
        #json_all = json.dumps(allSeries)
        with open(os.path.join(SEGMENTATION_PATH, "segmentMedian.json"), "w") as outfile:
            outfile.write(json_object)
        print("Writing done")
