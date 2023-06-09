import os

import netCDF4
import numpy as np
from helper.mds import mds
import time as t
from helper.pearson import pearson_corr_distance_matrix
import logging

def computeMDS(ENSEMBLE, OUT, SUBFOLDER = ""):
    for f in sorted(os.listdir(ENSEMBLE)):
        print(f)
        if SUBFOLDER != "":
            FIELD = os.path.join(os.path.join(ENSEMBLE, f), SUBFOLDER)
        else:
            FIELD = os.path.join(ENSEMBLE, f)
        VARIABLE_NAME = f
        logging.basicConfig(filename=OUT+'/full_'+f+'.log', level=logging.DEBUG)
        # Load Data
        data = np.empty((0,0))
        i = 0
        numberOfRuns = len(os.listdir(FIELD))
        for run in sorted(os.listdir(FIELD)):
            print("Loading run %s (%i)"%(run, (100.0*i)/numberOfRuns))
            path = os.path.join(FIELD, run)
            ff = netCDF4.Dataset(path)
            timelines = ff.variables[VARIABLE_NAME]
            timelines = np.transpose(timelines, axes=[1, 2, 0])
            timelines = timelines.reshape((timelines.shape[0] * timelines.shape[1], timelines.shape[2]))
            if(data.shape == (0,0)):
                data = timelines
            else:
                data = np.append(data, timelines, axis=1)
            ff.close()
            i=i+1
        # Distance matrix
        start_time = t.time()
        distance_matrix = pearson_corr_distance_matrix(timelines=data, lag=0)
        np.save(OUT+'/corr_full_'+f+'.npy', distance_matrix)
        distance_matrix = -(distance_matrix+1)*0.5+1

        print('... calculated full correlation in %s seconds' % (t.time() - start_time))
        logging.debug('calculated correlation in %s seconds' % (t.time() - start_time))

        Y, eigens = mds(distance_matrix, dimensions=3)
        np.save(OUT+'/y_full_'+f+'.npy', Y)
        np.save(OUT+'/eigens_full_'+f+'.npy', eigens)

        print('... calculated mds in %s seconds' % (t.time() - start_time))
        logging.debug('calculated mds in %s seconds' % (t.time() - start_time))
