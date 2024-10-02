# -*- coding: utf-8 -*-
"""Data Mining_Project Bisecting vs Kmeans(Sepal+SSE).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BixXHHPZtPRd0RruH-I6Jw0xlsfRWiBT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets,metrics
from sklearn.cluster import KMeans, BisectingKMeans

import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

from joblib import dump, load
sns.set()

cols = ['sepal_length', ' sepal_width', 'petal_length', 'petal_width', 'class']
df = pd.read_csv('/content/iris.csv', names=cols)
df.describe()

df = sns.load_dataset('iris')
sns.pairplot(df, hue ='species')
plt.show()

iris = datasets.load_iris()

df = iris.data[:, :2] # we only take the first two features.

"""# K-means Centroids"""

#plotting
plt.scatter(df[:,0],df[:,1])
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

km_iris = KMeans(n_clusters=4)
km_iris.fit(df)
print("Cluster Centroids:\n",km_iris.cluster_centers_)

# Calculate SSE (Sum of Squared Errors)

sse_per_cluster = []
labels = km_iris.labels_
for i in range(4):
    cluster_points = df[labels == i]
    cluster_center = km_iris.cluster_centers_[i]
    sse = np.sum((cluster_points - cluster_center) ** 2)
    sse_per_cluster.append(sse)
    print(f"SSE for cluster {i+1}: {sse}")

"""# Plotting Points"""

plt.scatter(df[:,0],df[:,1], c=km_iris.labels_, cmap='rainbow')
plt.scatter(km_iris.cluster_centers_[:,0] ,km_iris.cluster_centers_[:,1], color='black',marker="x")

plt.title("K Means", fontsize=14)
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

"""# Elbow Method for best number of K cluster"""

# Calculate sum of squared distances for different values of k
ssd = []
K = range(1, 11)  # Try different values of k from 1 to 10
for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(df)
    ssd.append(kmeans.inertia_)

# Plot the elbow
plt.plot(K, ssd, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()

"""# Compute Inter-cluster Distance"""

from sklearn.metrics.pairwise import euclidean_distances

print("Coordinates of Centroid:\n",km_iris.cluster_centers_)

dists = euclidean_distances(km_iris.cluster_centers_)
print("\nDistance between Centroids of four Clusters:\n",dists)

tri_dists = dists[np.triu_indices(4, 1)]
max_dist, avg_dist, min_dist = tri_dists.max(), tri_dists.mean(), tri_dists.min()

print("\nMaximum Distance:",max_dist)
print("\nAverage Distance:",avg_dist)
print("\nMinimum Distance:",min_dist)

"""# Compute Intra-cluster Distance:"""

print("\nCoordinates of Centroid:\n",km_iris.cluster_centers_)
distances = []
for i, centroid in enumerate(km_iris.cluster_centers_):
    data_array = []
    print("\nCoordinates of Centroid ",i,":",centroid)
    for (x,y) in df[km_iris.labels_ == i]:
      data_array.append([x,y])

    print("\nData points in Cluster",i,":", data_array)

    mean_distance = euclidean_distances(data_array,[centroid])
    print("\nDistance between all points and centroid in cluster",i,":\n",mean_distance)
    distances.append(mean_distance)

"""# Bisecting K-*means*"""

# Build and fit model with 4 clusters

bisect_means = BisectingKMeans(n_clusters=4,random_state=0).fit(df)

# Print model attributes:
print('Number of clusters: ', bisect_means.n_clusters)

#Define varaibles to be included in scatterdot:
y= bisect_means.labels_
centers = bisect_means.cluster_centers_

# Visualize the results using a scatter plot
plt.scatter(df[:, 0], df[:, 1], c=y, cmap = 'rainbow')
plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='black')
plt.title('Bisecting K-means')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

#Model built with Biggest Inertia:
bisect_means = BisectingKMeans(n_clusters=4, bisecting_strategy="biggest_inertia").fit(df)

#Print model attributes:
print('Number of clusters: ', bisect_means.n_clusters)
print('Model inertia: ', bisect_means.inertia_)

y= bisect_means.labels_
centers = bisect_means.cluster_centers_

# Calculate SSE for each cluster
sse = []
for i in range(bisect_means.n_clusters):
    cluster_points = df[y == i]
    cluster_center = centers[i]
    distances = np.linalg.norm(cluster_points - cluster_center, axis=1)
    cluster_sse = np.sum(distances ** 2)
    sse.append(cluster_sse)
    print(f'SSE for cluster {i+1}: {cluster_sse}')

total_sse = np.sum(sse)

# Visualize the results using a scatter plot
plt.scatter(df[:, 0], df[:, 1], c=y, cmap = 'rainbow')
plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='black')
plt.title('Bisecting K-means Strategy : highest sse ')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

#Model build with Largest Cluster:
bisect_means = BisectingKMeans(n_clusters=4,bisecting_strategy="largest_cluster").fit(df)

#Print model attributes:
print('Number of clusters: ', bisect_means.n_clusters)
print('Model inertia: ', bisect_means.inertia_)

y= bisect_means.labels_
centers = bisect_means.cluster_centers_

# Calculate SSE for each cluster
sse_per_cluster = np.zeros(bisect_means.n_clusters)
for i in range(bisect_means.n_clusters):
    cluster_points = df[y == i]
    cluster_center = centers[i]
    sse_per_cluster[i] = np.sum((cluster_points - cluster_center) ** 2)

# Print SSE for each cluster
for i, sse in enumerate(sse_per_cluster):
    print(f'SSE for cluster {i+1}: {sse}')

# Visualize the results using a scatter plot
plt.scatter(df[:, 0], df[:, 1], c=y, cmap='rainbow')
plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='black')
plt.title('Bisecting K-means Strategy: Largest Cluster')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

"""# K-means vs Bisecting K-means"""

# Number of cluster centers for KMeans and BisectingKMeans
n_clusters_list = [2, 3, 4, 5, 6]

# Algorithms to compare
clustering_algorithms = {
    "Bisecting K-Means": BisectingKMeans,
    "K-Means": KMeans,
}

# Make subplots for each variant
fig, axs = plt.subplots(len(n_clusters_list), len(clustering_algorithms), figsize=(20, 30))

for i, (algorithm_name, Algorithm) in enumerate(clustering_algorithms.items()):
    for j, n_clusters in enumerate(n_clusters_list):
        algo = Algorithm(n_clusters=n_clusters, n_init=3)
        algo.fit(df)

        if algorithm_name == "Bisecting K-Means":
            # Calculate total SSE for Bisecting K-Means
            sse = np.sum((df - algo.cluster_centers_[algo.labels_]) ** 2)
            axs[j, i].text(0.5, 0.9, f'Total SSE: {sse:.2f}', ha='center', transform=axs[j, i].transAxes)
        else:
            # Calculate individual SSE for K-Means
            sse = np.zeros(n_clusters)
            for k in range(n_clusters):
                cluster_points = df[algo.labels_ == k]
                sse[k] = np.sum((cluster_points - algo.cluster_centers_[k]) ** 2)
                axs[j, i].text(0.5, 0.9 - k * 0.05, f'Cluster {k+1} SSE: {sse[k]:.2f}', ha='center', transform=axs[j, i].transAxes)

        centers = algo.cluster_centers_
        axs[j, i].scatter(df[:, 0], df[:, 1], s=50, c=algo.labels_, cmap="rainbow")
        axs[j, i].scatter(centers[:, 0], centers[:, 1], marker='x', s=100, color='black')
        axs[j, i].set_title(f"{algorithm_name} : {n_clusters} clusters")

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
    ax.set_xticks([])
    ax.set_yticks([])

plt.show()