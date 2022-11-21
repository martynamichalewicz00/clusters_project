
selected_method = ["kmeans",
                   "spectral_clustering",
                   "agglomerate_ward",
                   "agglomerate_average",
                   "agglomerate_complete",
                   "agglomerate_single",
                   "kmeans_bisecting",
                   "dbscan"]

methods_description = ['General-purpose, even cluster size, flat geometry,not too many clusters, inductive.',
                       'Few clusters, even cluster size, non-flat geometry, transductive.',
                       'Many clusters, possibly connectivity constraints. This minimizes the sum '
                       'of squared differences within all clusters. ',
                       'Many clusters, possibly connectivity constraints. This minimizes the '
                       'maximum distance between observations of pairs of clusters.',
                       'Many clusters, possibly connectivity constraints. This minimizes the '
                       'average of the distances between all observations of pairs of clusters.',
                       'Many clusters, possibly connectivity constraints. This minimizes the '
                       'distance between the closest observations of pairs of clusters.',
                       'While K-Means clusterings are different when with increasing n_clusters, '
                       'Bisecting K-Means clustering build on top of the previous ones.',
                       'Non-flat geometry, uneven cluster sizes, outlier removal, transductive. '
                       'Number of clusters is minimum number of clusters'
                       ]

methods_names = ['K-Means',
                 'Spectral clustering',
                 'Hierarchical Ward',
                 'Hierarchical complete linkage',
                 'Hierarchical average linkage',
                 'Hierarchical single linkage',
                 'K-Means bisecting',
                 'DBSCAN']