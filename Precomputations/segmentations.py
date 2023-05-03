import numpy as np
import utils as u
import higra as hg
import os
import matplotlib.pyplot as plt
def colorLeaves(tree, altitudes, img, idx):
    children = tree.children(idx)
    if(altitudes[idx] > 0):
        for child in children:
            colorLeaves(tree, altitudes, img, child)
    else:
        for c in children:
            x = c % img.shape[1]
            y = int(c / img.shape[1])
            img[y, x] = idx
            
def computeSegmentation(MDS_POINTS_PATH, SHAPE, CIRCULAR, SOBEL, OUT_PATH, roll=False):
    numSeg = {} # Stores the number of segments on the lowest level of detail
    # Iterate over fields
    files = [f for f in os.listdir(MDS_POINTS_PATH) if "y_full" in f]
    for f in sorted(files):
        field = f[7:-4]
        field_variable = field
        if "Anomaly" in field:
            field_variable = field[:-7]
        print(field_variable)

        # Load data
        mds_points = np.load(os.path.join(MDS_POINTS_PATH, f))
        image_shape = SHAPE
        mds_points = u.normalize_point(mds_points)
        mds_image = np.reshape(mds_points, (*image_shape, mds_points.shape[-1]))

        # Compute hierarchical segmentation
        graph = hg.get_4_adjacency_graph(SHAPE)
        grad_img = None
        if (CIRCULAR):
            stiched_mds_image = np.hstack((mds_image,) * 3)
            stitched_grad_img = u.gradient_image(stiched_mds_image)

            stitched_grad_img = np.transpose(stitched_grad_img, (1, 2, 0))
            stitched_grad_img = np.linalg.norm(stitched_grad_img, axis=2)
            grad_img = stitched_grad_img[:, SHAPE[1]:2 * SHAPE[1]]

            sources = np.arange(0, graph.num_vertices(), SHAPE[1])
            targets = np.arange(SHAPE[1] - 1, graph.num_vertices(), SHAPE[1])
            graph.add_edges(sources, targets)

        if (SOBEL):
            if (grad_img.any() == None):
                grad_img = u.gradient_image(mds_image)
                grad_img = np.transpose(grad_img, (1, 2, 0))
                grad_img = np.linalg.norm(grad_img, axis=2)
            edge_weights = hg.weight_graph(graph, grad_img, hg.WeightFunction.mean)
        else:
            edge_weights = hg.weight_graph(graph, mds_points, hg.WeightFunction.L2)
        tree, altitudes = hg.watershed_hierarchy_by_area(graph, edge_weights)

        # Create image to show the hierarchy on the lowest level of detail
        cut_helper = hg.HorizontalCutExplorer(tree, altitudes)
        #print(cut_helper.num_cuts())
        cut = cut_helper.horizontal_cut_from_index(cut_helper.num_cuts()-5)
        img = np.zeros(SHAPE)
        colorLeaves(tree, altitudes, img, tree.root())
        #plt.imshow(img)
        #plt.title(field)
        if roll:
            print("rolling")
            img = np.roll(img, int(img.shape[1] / 2), axis=1)
        np.save(os.path.join(OUT_PATH, field+".npy"), img)
        plt.imsave(os.path.join(OUT_PATH, field+".png"), img)
        #plt.show()
        nodes = cut.nodes()
        numSeg[field] = len(np.unique(img))
    print(numSeg)
