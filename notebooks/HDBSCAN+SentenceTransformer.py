import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import json 

# Step 1: Read CSV data from a file
csv_file_path = 'labeled_dummy_dataset.csv'  # Replace this with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Extract texts and true labels
texts = df['Text'].tolist()
true_labels = df['Label'].tolist()

# Step 2: Generate Sentence Embeddings
print("Generating sentence embeddings...")
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(texts)
embeddings_array = np.array(embeddings)

# Step 3: Dimensionality Reduction with UMAP
print("Reducing dimensions with UMAP...")
reducer = umap.UMAP(n_components=10, random_state=42)
embeddings_reduced = reducer.fit_transform(embeddings_array)

# Step 4: Apply HDBSCAN Clustering
print("Applying HDBSCAN clustering...")
hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
predicted_labels = hdbscan_cluster.fit_predict(embeddings_reduced)

# Step 5: Organize Documents by Predicted Cluster Labels
clusters = {}
for cluster_label, text, true_label in zip(predicted_labels, texts, true_labels):
    # Use the integer cluster_label directly as the key
    if cluster_label not in clusters:
        clusters[cluster_label] = []
    clusters[cluster_label].append({'Text': text, 'TrueLabel': true_label})

# Step 6: Package Clusters into JSON Format
packaged_data = []
for cluster_id, docs in clusters.items():
    cluster_data = {
        "cluster_id": int(cluster_id),
        "documents": docs
    }
    packaged_data.append(cluster_data)

# Convert to JSON
json_output = json.dumps(packaged_data, indent=4)
print(json_output)

# Save to a file if needed
with open("devan_packaged_clusters.json", "w") as file:
    file.write(json_output)
