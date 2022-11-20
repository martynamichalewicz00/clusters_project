from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
import pandas as pd


class ClusterAnalysis:
    labels = []
    data_frame = pd.DataFrame()

    def __init__(self, data, number_of_clusters=2, method="kmeans", labels=0):
        self.data = data
        self.number_of_clusters = number_of_clusters
        self.method = method
        self.labels = labels

        self.make_labels(data, number_of_clusters, method, labels)
        self.whole_data_frame(self.data)

    def make_labels(self, data, number_of_clusters, method, labels):

        self.data = pd.read_csv(data, sep=";")

        if labels:
            self.data = self.data.drop(self.data.columns[[0]], axis=1)

        self.data = self.numeric_and_categorical()
        self.change_method(method, number_of_clusters)

    def change_method(self, method, number_of_clusters):
        if method == "kmeans":
            self.labels = KMeans(n_clusters=number_of_clusters, random_state=0).fit(self.data)
        elif method == "spectral_clustering":
            self.labels = SpectralClustering(n_clusters=number_of_clusters, random_state=0).fit(self.data)
        elif method == "agglomerative_clustering":
            self.labels = AgglomerativeClustering().fit(self.data)

    def numeric_and_categorical(self):

        data_numeric = pd.DataFrame(self.data)
        data_categorical = pd.DataFrame(self.data)

        for i in data_numeric._get_numeric_data().columns.values.tolist():
            del data_numeric[i]

        for i in data_numeric:
            del data_categorical[i]

        data_numeric = self.coding_categorical(data_numeric)
        data_categorical = data_categorical.join(data_numeric)

        return data_categorical

    def coding_categorical(self, data):

        original_values = self.original_values(data)
        data = self.replace_from_categorical(data, original_values)
        return data

    def whole_data_frame(self, data):
        labels = list(self.labels.labels_)
        labels = pd.DataFrame(labels, columns=["cluster"])
        self.data_frame = pd.concat([data, labels], axis=1)

    @staticmethod
    def original_values(data):
        original_values = []
        names_of_columns = list(data)
        for column_name in names_of_columns:
            original_values.append(data[column_name].value_counts())
        return original_values

    @staticmethod
    def replace_from_categorical(data, original_values):
        for i in range(len(original_values)):
            names_to_replace = []
            for j in range(len(original_values[i])):
                names_to_replace.append((original_values[i].index[j]))
            data = data.replace(names_to_replace, range(1, len(names_to_replace) + 1))
        return data


c = ClusterAnalysis('iris.csv', 3, "kmeans", 1)
print(c.data_frame)
