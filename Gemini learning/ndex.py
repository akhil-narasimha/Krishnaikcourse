import numpy as np

# Our tiny database: 6 vectors (imagine each is a document)
vectors = np.array([
    [1.0, 0.1],   # cat
    [0.9, 0.2],   # kitten
    [0.1, 1.0],   # dog
    [0.2, 0.9],   # puppy
    [0.8, 0.3],   # feline
    [0.3, 0.8]    # hound
], dtype=np.float32)

print("Database:")
print(vectors)

# LSH magic: draw 2 random lines
np.random.seed(42)
num_bits = 2
random_vectors = np.random.randn(num_bits, 2)
random_vectors /= np.linalg.norm(random_vectors, axis=1, keepdims=True)

def lsh_hash(vec):
    projections = np.dot(random_vectors, vec)
    bits = (projections > 0).astype(int)
    return ''.join(map(str, bits))

# Put every vector into its bucket
buckets = {}
for i, v in enumerate(vectors):
    h = lsh_hash(v)
    if h not in buckets:
        buckets[h] = []
    buckets[h].append((i, v))

print("\nBuckets created:")
for h, items in buckets.items():
    print(f"Bucket {h}: {len(items)} items")
    for idx, vec in items:
        print(f"   Vector {idx}: {vec}")

# Search time!
query = np.array([0.95, 0.15])   # something like "cat"
q_hash = lsh_hash(query)
print(f"\nQuery hash: {q_hash}")

candidates = buckets.get(q_hash, [])
print(f"Only {len(candidates)} candidates to check!")

# Quick exact check on candidates only
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

similarities = [(idx, cosine_sim(query, vec)) for idx, vec in candidates]
similarities.sort(key=lambda x: x[1], reverse=True)
print("Best matches:")
for idx, sim in similarities:
    print(f"Vector {idx} → similarity {sim:.3f}")



#IVF


import numpy as np
from scipy.cluster.vq import kmeans, vq

# Same database
vectors = np.array([
    [1.0, 0.1], [0.9, 0.2], [0.1, 1.0],
    [0.2, 0.9], [0.8, 0.3], [0.3, 0.8]
], dtype=np.float32)

# Create 2 smart districts
num_clusters = 2
centroids, _ = kmeans(vectors, num_clusters, seed=42)

print("District centers (centroids):")
print(centroids)

# Build districts
cluster_ids, _ = vq(vectors, centroids)
districts = [[] for _ in range(num_clusters)]
for i, cid in enumerate(cluster_ids):
    districts[cid].append((i, vectors[i]))

print("\nDistricts:")
for cid, items in enumerate(districts):
    print(f"District {cid}: {len(items)} vectors")

# Query
query = np.array([0.95, 0.15])
dist_to_centers = np.linalg.norm(centroids - query, axis=1)
nearest_district = np.argmin(dist_to_centers)

print(f"\nQuery goes to District {nearest_district}")
candidates = districts[nearest_district]

# Same similarity check as before
similarities = [(idx, cosine_sim(query, vec)) for idx, vec in candidates]  # reuse cosine_sim from before
similarities.sort(key=lambda x: x[1], reverse=True)
print("Best matches in this district:")
for idx, sim in similarities:
    print(f"Vector {idx} → similarity {sim:.3f}")


import numpy as np
import networkx as nx

vectors = np.array([[1.0,0.1],[0.9,0.2],[0.1,1.0],[0.2,0.9],[0.8,0.3],[0.3,0.8]])
labels = ['cat0','cat1','dog0','dog1','cat2','dog2']

G = nx.Graph()
for i in range(len(vectors)):
    G.add_node(i, vector=vectors[i], label=labels[i])

# Connect nearest neighbors (bottom layer)
for i in range(len(vectors)):
    sims = [(j, cosine_sim(vectors[i], vectors[j])) for j in range(len(vectors)) if j != i]
    sims.sort(key=lambda x: x[1], reverse=True)
    for j, _ in sims[:2]:
        G.add_edge(i, j)

# Promote 2 nodes to top layer and connect them
G.nodes[0]['layer'] = 1
G.nodes[2]['layer'] = 1
G.add_edge(0, 2)

# Search: start top → zoom down
query = np.array([0.95, 0.15])
current = 0
print("Start top layer →", labels[current])
# (greedy steps on layers - simplified)
print("Zoom down... final best:", labels[current])