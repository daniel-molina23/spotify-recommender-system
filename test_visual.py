#%%
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns

data = pd.read_csv("corrected_norm_data.csv.zip", compression="zip")
feat_cols = ['acousticness','danceability','energy','instrumentalness','key','loudness','popularity','speechiness','tempo']
#%%
# print(data.shape) # 170,391 X 9

# For reproducability of the results
np.random.seed(42)
rndperm = np.random.permutation(data.shape[0])

#%%
pca = PCA(n_components=2)
pca_result = pca.fit_transform(data[feat_cols].values)

data['pca-one'] = pca_result[:,0]
data['pca-two'] = pca_result[:,1]
data['pca-three'] = pca_result[:,2]

print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
# print(data.head())


plt.figure(figsize=(16,10))
sns.scatterplot(
    x="pca-one", y="pca-two",
    hue=None,
    palette=sns.color_palette("hls", 10),
    data=data.loc[rndperm[:10000],:],
    legend="full",
    alpha=0.3
)
plt.show()
# %%
ax = plt.figure(figsize=(16,10)).gca(projection='3d')
ax.scatter(
    xs=data.loc[rndperm[:10000],:]["pca-one"], 
    ys=data.loc[rndperm[:10000],:]["pca-two"], 
    zs=data.loc[rndperm[:10000],:]["pca-three"],
    cmap='tab10'
)
ax.set_xlabel('pca-one')
ax.set_ylabel('pca-two')
ax.set_zlabel('pca-three')
plt.show()
# %%

N = 10000 # taking the first 10,000 numbers from the random permutation of all the values

df_subset = data.loc[rndperm[:N],:].copy() # copy first 10000
data_subset = df_subset[feat_cols].values

# parameter info: https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=1000)
# metrics can be: distance function can be ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulsinski’, ‘mahalanobis’, ‘matching’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’
    # default: metric=euclidean             maybe try metric=cosine, or jaccard

tsne_results = tsne.fit_transform(data_subset)

#%%
df_subset['tsne-2d-one'] = tsne_results[:,0]
df_subset['tsne-2d-two'] = tsne_results[:,1]
plt.figure(figsize=(16,10))
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    hue=None,
    palette=sns.color_palette("hls", 10),
    data=df_subset,
    legend="full",
    alpha=0.3
)
# %%
# from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_subset[feat_cols]) # makes mean of 0 and stdev of 1
# scaled_features = df_subset[feat_cols] # normalized

k_means_kwargs = {
    'init':"random", 
    'n_init':10, 
    'max_iter':300, 
    'random_state':42
}
# Initialize by placing some centroid on either artist or genre for k-means
# make labels for validation: label the data
sse = []
silhouette = []
k_clusters = range(2,16)

for k in k_clusters:
    kmeans = KMeans(n_clusters=k, **k_means_kwargs)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)
    silhouette.append(silhouette_score(scaled_features, kmeans.labels_, metric='euclidean'))
    print("k=%d is done!"%(k))


figure, axis = plt.subplots(2, 1)

plt.style.use("fivethirtyeight")
axis[0].plot(k_clusters,sse)
axis[0].set_xticks(k_clusters)
axis[0].set_xlabel("Number of Clusters")
axis[0].set_ylabel("SSE")

axis[1].plot(k_clusters,silhouette)
axis[1].set_xticks(k_clusters)
axis[1].set_xlabel("Number of Clusters")
axis[1].set_ylabel("Silhouette Score")

plt.show()
# %%
