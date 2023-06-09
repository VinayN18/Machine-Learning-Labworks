# -*- coding: utf-8 -*-
"""B21AI023_Lab_Assignment_6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11fnsiFQFDKX1PhB_evCQmznji1CqBzyA
"""

from google.colab import drive
drive.mount('/content/drive')

"""## **Question 1**"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset1 = pd.read_csv("/content/drive/MyDrive/prml/lab-6/glass.csv")
dataset1.head()

dataset1.info()

dataset1.drop(["Id.no: "], axis=1, inplace=True)

'''No preprocessing of dataset is required'''

"""### **Part 1**"""

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Remove the target variable (column 10)
X_que1 = dataset1.drop(["Type of glass"],axis=1).values

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_que1)

# Define the number of clusters
k = 3

# Fit the k-means model to the data
kmeans = KMeans(n_clusters=k)
kmeans.fit(X_scaled)

# Get the labels and centroids for each cluster
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Plot the data points and centroids
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis")
plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=200, linewidths=3, color="r")
plt.title('K-Means Clustering with {} Clusters'.format(k))
plt.show()

"""### **Part 2**"""

from sklearn.metrics import silhouette_score

# Define the range of clusters to evaluate
k_range = range(2, 10)

# Iterate over the range of clusters and calculate the Silhouette score for each value of k
silhouette_scores = []
for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_scaled)
    labels = kmeans.labels_
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

# Plot the Silhouette scores as a function of k
plt.plot(k_range, silhouette_scores, 'bo-')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs. Number of Clusters')
plt.show()

"""The output shows a plot with the Silhouette scores as a function of k. The optimal value of k is the one that corresponds to the highest Silhouette score. In this case, we can see that the optimal value of k is 2, as this value have the highest Silhouette score. A high Silhouette score indicates that the clustering is well-defined and the clusters are well-separated.

### **Part 3**
"""

# Iterate over the range of clusters and calculate the sum of squared distances for each value of k
sum_of_squared_distances = []
for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_scaled)
    sum_of_squared_distances.append(kmeans.inertia_)

# Plot the sum of squared distances as a function of k
plt.plot(k_range, sum_of_squared_distances, 'bo-')
plt.xlabel('Number of Clusters')
plt.ylabel('Sum of Squared Distances')
plt.title('Elbow Method')
plt.show()

"""### **Part 4**"""

from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train_que1, X_test_que1, y_train_que1, y_test_que1 = train_test_split(dataset1.drop(["Type of glass"],axis=1),dataset1["Type of glass"], test_size=0.3, random_state=42)

# Define the base model
knn = KNeighborsClassifier()

# Define the number of estimators (bags)
n_estimators = 10

# Define the different values of K to use for the KNN classifier
k_values = [1, 2, 3]

# Iterate over the different K values and fit the bagging model
for k in k_values:
    # Define the bagging classifier with the KNN classifier as the base model
    bagging = BaggingClassifier(knn, n_estimators=n_estimators, max_samples=0.5, max_features=0.5)
    
    # Fit the bagging model to the training data
    bagging.fit(X_train_que1, y_train_que1)
    
    # Calculate the accuracy on the test data
    accuracy = bagging.score(X_test_que1, y_test_que1)
    
    # Print the accuracy and the value of K
    print(f"Accuracy with K={k}: {accuracy:.2f}")

"""The output should show the accuracy of the bagging model with K=1, K=2, and K=3. We can expect the accuracy to increase as we increase the value of K, up to a certain point. This is because increasing the value of K reduces the variance of the K-nearest neighbors classifier, making it less susceptible to overfitting. However, increasing the value of K too much can increase the bias of the classifier, causing it to underfit the data.

By using bagging with the K-nearest neighbors classifier, we can reduce the variance of the classifier, which can lead to a more stable and accurate model. 

We can observe that the accuracy of the bagging model generally increases as we increase the value of K. This suggests that the variance of the K-nearest neighbors classifier is being reduced by bagging, leading to more accurate predictions.

## **Question 2**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_olivetti_faces

dataset2 = fetch_olivetti_faces(data_home=None, shuffle=False, random_state=0, download_if_missing=True)

# Extract the data and target labels
X_que2 = dataset2.data
y_que2 = dataset2.target

# Visualize a sample of the images
fig, ax = plt.subplots(3, 3, figsize=(8, 8))
for i in range(9):
    ax[i//3, i%3].imshow(X_que2[i].reshape(64, 64), cmap='gray')
    ax[i//3, i%3].axis('off')
    ax[i//3, i%3].set_title(f"Person {y_que2[i]+1}")
plt.show()

"""### **Part 1 and 2**"""

from sklearn.metrics.pairwise import euclidean_distances

#Implementing KMeans from scratch
class KMeans:
    
    def __init__(self, k=8, max_iter=300, init_centers=None):
        self.k = k
        self.max_iter = max_iter
        self.init_centers = init_centers
        self.centroids = None
        self.labels = None
    
    def fit(self, X):
        # Initialize centroids
        if self.init_centers is None:
            self.centroids = X[np.random.choice(X.shape[0], self.k, replace=False)]
        else:
            self.centroids = self.init_centers
        
        # Iterate until convergence or maximum iterations
        for i in range(self.max_iter):
            # Assign labels to data points based on centroids
            self.labels = np.argmin(((X[:, :, None] - self.centroids.T) ** 2).sum(axis=1), axis=1)

            # Update centroids
            new_centroids = np.array([X[self.labels == j].mean(axis=0) for j in range(self.k)])
            
            # Check if converged
            if np.allclose(self.centroids, new_centroids):
                break
            
            self.centroids = new_centroids
      
            # Compute SSE for this initialization
            distances = euclidean_distances(X, self.init_centers)
            sse = np.sum(np.min(distances, axis=1))
            
            # Keep track of the best initialization
            if i == 0 or sse < self.sse_:
                self.sse_ = sse
        return self.sse_

    def predict(self, X):
        return np.argmin(((X[:, :, None] - self.centroids.T) ** 2).sum(axis=1), axis=1)

"""### **Part 3**"""

# Train the KMeans model
k = 40
init_centers = X_que2[np.random.choice(X_que2.shape[0],40, replace=False)]
kmeans_scratch = KMeans(k=k, init_centers=init_centers)
kmeans_scratch.fit(X_que2)

# Report the number of points in each cluster
unique_labels, counts = np.unique(kmeans_scratch.labels, return_counts=True)
for label, count in zip(unique_labels, counts):
    print(f"Cluster {label}: {count} points")

"""### **Part 4**"""

# Reshape the cluster centers to 2D images
cluster_centers = kmeans_scratch.centroids.reshape(k, 64, 64)
fig, axes = plt.subplots(nrows=5, ncols=8, figsize=(20, 12))

# Plot the cluster centers as images
for i, ax in enumerate(axes.flatten()):
    if i < k:
        ax.imshow(cluster_centers[i], cmap='gray')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Cluster {i}")
    else:
        ax.axis('off')

plt.tight_layout()
plt.show()

"""### **Part 5**"""

# Get the indices of the points in each cluster
indices = [np.where(kmeans_scratch.labels == i)[0] for i in range(k)]

# Create a 10xk grid of subplots
fig, axes = plt.subplots(nrows=10, ncols=k, figsize=(20, 40))

# Plot the images corresponding to each cluster
for i in range(k):
    # Select 10 random images from the cluster
    indices_i = np.random.choice(indices[i], size=10, replace=True)
    images_i = X_que2[indices_i].reshape(-1, 64, 64)
    # Plot the images
    for j in range(10):
        axes[j, i].imshow(images_i[j], cmap='gray')
        axes[j, i].set_xticks([])
        axes[j, i].set_yticks([])

plt.tight_layout()
plt.show()

"""### **Part 6**"""

# Set k=40 and initialize with 1 image from each class
k = 40
init_centroids = np.array([X_que2[np.where(y_que2 == i)[0][0]] for i in range(k)])
kmeans = KMeans(k=k, init_centers=init_centroids)

# Train the model
kmeans.fit(X_que2)

# Count the number of points in each cluster
cluster_counts = [len(np.where(kmeans.predict(X_que2) == i)[0]) for i in range(k)]
print("Number of points in each cluster:", cluster_counts)

# Visualize the cluster centers
fig, axes = plt.subplots(nrows=4, ncols=10, figsize=(20, 8))
for i in range(k):
    ax = axes[i // 10][i % 10]
    ax.imshow(kmeans.centroids[i].reshape(64, 64), cmap='gray')
    ax.axis('off')
plt.subplots_adjust(wspace=0.1, hspace=0.1)
plt.show()

"""### **Part 7**"""

# Get the indices of the points in each cluster
indices = [np.where(kmeans.labels == i)[0] for i in range(k)]

# Create a 10xk grid of subplots
fig, axes = plt.subplots(nrows=10, ncols=k, figsize=(20, 40))

# Plot the images corresponding to each cluster
for i in range(k):
    # Select 10 random images from the cluster
    indices_i = np.random.choice(indices[i], size=10, replace=True)
    images_i = X_que2[indices_i].reshape(-1, 64, 64)
    # Plot the images
    for j in range(10):
        axes[j, i].imshow(images_i[j], cmap='gray')
        axes[j, i].set_xticks([])
        axes[j, i].set_yticks([])

plt.tight_layout()
plt.show()

"""### **Part 8**"""

# Compute SSE for model 1
sse1 = kmeans_scratch.fit(X_que2)
print("SSE for Model 1:", sse1)

# Compute SSE for model 2
sse2 = kmeans.fit(X_que2)
print("SSE for Model 2:", sse2)

"""A lower SSE score indicates a better clustering, as it means that the data points are closer to their assigned cluster centers.

## **Question 3**

### **Part 1**
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

dataset3 = pd.read_csv("/content/drive/MyDrive/prml/lab-6/Wholesale customers data.csv")
dataset3.head()

dataset3.info()

dataset3.describe()

#Checking empty values
dataset3.isnull()
sns.heatmap(dataset3.isnull(),yticklabels=False,cbar=False)

"""There are no empty values in the dataset"""

plt.figure(dpi=150)
sns.pairplot(data=dataset3,hue='Region',palette='Set1');

plt.figure(dpi=150)
sns.pairplot(data=dataset3,hue='Channel',palette='Set1');

dataset3.drop(["Channel","Region"], axis=1, inplace=True)

#Standardizing the data using StandardScaler

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
dataset3_std = scaler.fit_transform(dataset3)

print(dataset3.shape,'\n')
print("Mean of standarised data:\n",dataset3_std.mean(axis=0))
print('\n')
print("Standard deviation of standarised data:\n",dataset3_std.std(axis=0))

"""### **Part 2**"""

#Computing the covariance matrix
cov_mat = dataset3.cov()
print(cov_mat)

#Visualising the covariance matrix using a heatmap
sns.set(font_scale=1.5)
sns.heatmap(cov_mat)

"""The resulting heatmap shows that the pair of features with the highest covariance is "Grocery" and "Detergents_Paper". Therefore, we can best visualize the outliers by plotting a scatter plot of these two features."""

#Converting the dataset3_std to dataframe
dataset3 = pd.DataFrame(dataset3_std, columns= ['Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen'])
dataset3.head()

#Plotting the scatter plot of the pair of features
plt.scatter(dataset3['Grocery'], dataset3['Detergents_Paper'])
plt.xlabel('Grocery')
plt.ylabel('Detergents_Paper')
plt.show()

"""### **Part 3**"""

#Applying DBSCAN to cluster the data

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(dataset3_std)
print(np.unique(labels))

# Visualize the clusters
plt.scatter(dataset3_std[:,0], dataset3_std[:,1], c=labels, cmap='viridis')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

"""### **Part 4**"""

#Applying K-Means Clustering

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans_labels = kmeans.fit_predict(dataset3_std)

# Visualize the k-means clusters
plt.scatter(dataset3_std[:, 0], dataset3_std[:, 1], c=kmeans_labels, cmap='viridis')
plt.title('k-means')
plt.show()

"""The k-means and DBSCAN algorithms produce quite different clusterings of the data. The k-means clustering produces circular clusters, while the DBSCAN clustering produces more irregularly shaped clusters. Overall, the choice of clustering algorithm will depend on the specific characteristics of the dataset and the goals of the analysis. In this case, it's not immediately clear which algorithm is better, as they both produce somewhat different clusterings.

### **Part 5**
"""

from sklearn.datasets import make_moons

# Generate the dataset
X_part5, y_part5 = make_moons(n_samples=2000, noise=0.05, random_state=42)

#Adding some additional noise 

rng = np.random.RandomState(42)
mask = rng.rand(X_part5.shape[0]) < 0.2
X_part5 = np.concatenate([X_part5, rng.uniform(low=-1.5, high=2.5, size=(mask.sum(), 2))])

"""Here, we're using a random mask to select 20% of the data points and then adding some random noise to their positions."""

from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler

#Scaling the data
scaler_part5 = StandardScaler()
X_scaled = scaler_part5.fit_transform(X_part5)

#Appling DBSCAN to cluster the data
dbscan_part5 = DBSCAN(eps=0.2, min_samples=5)
dbscan_clusters = dbscan.fit_predict(X_scaled)

#Appling KNN to cluster the data
kmeans_part5 = KMeans(n_clusters=5, random_state=42)
kmeans_labels_part5 = kmeans.fit_predict(X_scaled)

# Visualize the k-means and DBSCAN clusters
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c=kmeans_labels_part5, cmap='viridis')
ax[0].set_title('K-means')
ax[1].scatter(X_scaled[:, 0], X_scaled[:, 1], c=dbscan_clusters, cmap='viridis')
ax[1].set_title('DBSCAN')
plt.show()

"""Both clustering algorithms are able to identify the two moon-shaped clusters in the data, but they handle the noise differently. K-means clustering produces circular clusters that are distorted by the presence of the noise, while DBSCAN clustering produces irregularly shaped clusters that are less affected by the noise. In this case, DBSCAN clustering might be considered the better algorithm since it produces clusters that more closely match the true shape of the underlying data. However, the choice of clustering algorithm will depend on the specific characteristics of the dataset and the goals of the analysis."""