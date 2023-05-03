from similarityImages import computeMDS
from segmentations import computeSegmentation
from extractSegmentBoundaries import computeBoundaries
from createImage import createImage
from computeDistanceMatrix import computeDistanceMatrix
from segmentMedian import segmentMedian
from correlations import correlations

# ------------------------------------------------------------------------------#
# Adapt the following data to your dataset                                      #
# ------------------------------------------------------------------------------#
ENSEMBLE = "../ArtificialData" # Path to ensemble data
TMP_PATH = "../tmp_artificial/" # Path to store temporary data
FIELDS =  ['f1', 'f2'] # Name of the fields
SHAPE = (16, 24) # Shape of the spatial domain
CIRCULAR = True # Is the data circular (like e.g. the earth?)
SOBEL = False # Should the Sobel filter be used for computing the segmentation?
NUM_RUNS = 10 # Number of simulation runs
NUM_TIME_STEPS = 300 # Number of time steps per simulation run

computeMDS(ENSEMBLE, TMP_PATH)
print("MDS done")
computeSegmentation(TMP_PATH, SHAPE, CIRCULAR, SOBEL, TMP_PATH)
print("Segmentation done")
computeBoundaries(FIELDS, TMP_PATH)
print("Boundaries done")
createImage(TMP_PATH, SHAPE)
print("Image done")
computeDistanceMatrix(ENSEMBLE, TMP_PATH, TMP_PATH, NUM_TIME_STEPS)
print("Distance done")
segmentMedian(ENSEMBLE, TMP_PATH, NUM_TIME_STEPS, SUBFOLDER = "", outOfCore=True, numMembers = 10)
print("Median done")
correlations(ENSEMBLE, TMP_PATH, NUM_TIME_STEPS)
