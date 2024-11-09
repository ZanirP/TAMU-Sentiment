from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import umap
import hdbscan
import matplotlib.pyplot as plt
import numpy as np

# Updated corpus of documents with more distinct topics
documents = [
    # Football-related
    "Aggies win football game in thrilling overtime!",
    "The quarterback threw an amazing pass to secure the win.",
    "Fans stormed the field after the incredible victory!",
    "The Aggies football team is training hard for the next big game.",
    "A heartbreaking loss for the Aggies in the final seconds.",
    "Coach praises the defense for their strong performance.",
    "Aggies fans are hopeful for the championship this year.",
    "Exciting game day with tailgates and Aggie pride!",
    "Star running back breaks record for most yards in a game.",
    "Football game against rivals ends in a dramatic tie.",
    "The crowd erupted as the Aggies scored the game-winning touchdown.",
    "Defensive strategy played a crucial role in last night’s game.",
    "Aggie football players dedicated the win to their loyal fans.",
    "Team morale is high as they prepare for the season's biggest match.",
    "Aggies are reviewing game footage to improve tactics.",
    "The kicker made a 50-yard field goal under intense pressure.",
    "Injuries have affected key players, but the team remains strong.",
    "Football analysts are impressed with the Aggies’ performance.",
    "The offensive line showed great improvement in the latest game.",
    "Aggies football merchandise sold out after the big win!",

    # Career Fair-related
    "Massive turnout for the TAMU career fair.",
    "Companies at the career fair are actively recruiting Aggies.",
    "The job fair was packed with companies and students.",
    "Students dressed in their best suits for networking.",
    "Career fair workshops are helping students prepare.",
    "Exciting internship opportunities announced at the fair.",
    "The career fair was a great opportunity to meet employers.",
    "Aggies land interviews after networking at the career fair.",
    "Recruiters were impressed by the Aggie spirit and readiness.",
    "Companies like Amazon and Google attended the career fair.",
    "New graduates are hopeful for positions offered at the fair.",
    "Career advisors provided resume tips and interview strategies.",
    "Tech companies showcased their latest innovations at the fair.",
    "The career fair featured panels with industry professionals.",
    "Students received job offers on the spot from several companies.",
    "Engineering majors were in high demand at the career fair.",
    "The career center organized mock interviews for attendees.",
    "Networking events followed the main career fair activities.",
    "Business cards were exchanged rapidly as connections were made.",
    "Workshops focused on how to negotiate job offers effectively.",

    # Research-related
    "New research breakthroughs at Texas A&M.",
    "Innovative research on climate change solutions.",
    "Aggies develop new technology for sustainable energy.",
    "The research lab is making advancements in AI.",
    "Texas A&M researchers publish a groundbreaking study.",
    "Research funding awarded for biomedical innovation.",
    "Graduate students are presenting their research findings.",
    "Collaborative research projects between departments are thriving.",
    "Faculty members win awards for their research contributions.",
    "Exciting developments in quantum computing research.",
    "Agricultural research is revolutionizing farming practices.",
    "The university is a leader in robotics and automation studies.",
    "A research team discovers new ways to treat rare diseases.",
    "Breakthroughs in genetics research are making headlines.",
    "Researchers are developing a new material stronger than steel.",
    "Physics students experiment with groundbreaking theories.",
    "Biology lab discovers a new species of bacteria in the wild.",
    "Economics research is influencing policy decisions nationwide.",
    "Chemistry breakthroughs have potential for major applications.",
    "Research in renewable energy is reducing carbon footprints.",

    # Basketball-related
    "Aggies lose a close basketball match.",
    "Texas A&M basketball team wins the championship!",
    "The coach strategizes for the upcoming basketball season.",
    "Basketball fans fill the arena for an intense game.",
    "Star player scores a career-high in the basketball match.",
    "Aggies basketball team prepares for March Madness.",
    "The team's defense played exceptionally well in the game.",
    "A buzzer-beater shot leads the Aggies to victory!",
    "Fans cheer as the Aggies dominate on the basketball court.",
    "Preseason basketball training camp starts next week.",
    "The team is focusing on building a strong offense this year.",
    "Basketball practice intensifies as the season opener nears.",
    "New recruits are showing promise in early scrimmages.",
    "The coach emphasizes teamwork and discipline at practice.",
    "Players are reviewing game footage to improve techniques.",
    "Aggies basketball is featured in national sports coverage.",
    "The team's captain motivates everyone to push harder.",
    "Home games are expected to draw record-breaking crowds.",
    "Aggies basketball alumni share their success stories.",
    "The rivalry game is highly anticipated by fans and players.",

    # Spam or irrelevant content
    "Win a free iPhone by clicking this link!",
    "Best deals on car insurance you can find today!",
    "Don't miss out on this amazing opportunity, click now!",
    "Congratulations, you've won a $500 gift card!",
    "Limited-time offer: Get rich quick with this scheme.",
    "Download this app to make money fast!",
    "Earn cash easily from home with no effort.",
    "Invest in cryptocurrency and watch your money grow!",
    "Free vacation to the Bahamas, just pay a small fee!",
    "Join our online community to make easy money!",
    "Your computer is at risk! Download this antivirus software.",
    "Act now to secure your spot in this money-making webinar!",
    "Get a free gift just by signing up for our service.",
    "Lose weight fast with this one simple trick!",
    "Earn $1000 a day with this foolproof method!",
    "Work from home and earn big bucks without any skills!",
    "Discover the secret to instant financial freedom!",
    "You won't believe this shocking health discovery!",
    "Click here for the ultimate guide to success!",
    "Get your credit score checked for free—no strings attached!"
]

# Step 1: Generate Sentence Embeddings
print("Generating sentence embeddings...")
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(documents)
embeddings_array = np.array(embeddings)

# Step 2: Dimensionality Reduction with UMAP
print("Reducing dimensions with UMAP...")
reducer = umap.UMAP(n_components=10, random_state=42)
embeddings_reduced = reducer.fit_transform(embeddings_array)

# Step 3: Apply HDBSCAN Clustering
print("Applying HDBSCAN clustering...")
hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
labels_hdbscan = hdbscan_cluster.fit_predict(embeddings_reduced)

# Step 4: Organize Documents by Cluster
clusters_hdbscan = {}
for label, doc in zip(labels_hdbscan, documents):
    if label == -1:
        continue  # Skip outliers
    if label not in clusters_hdbscan:
        clusters_hdbscan[label] = []
    clusters_hdbscan[label].append(doc)

# Step 5: Display Clusters
print("\nDocuments organized by HDBSCAN clusters:")
for cluster_id, docs in clusters_hdbscan.items():
    print(f"\nCluster {cluster_id} ({len(docs)} documents):")
    for doc in docs:
        print(f"  - {doc}")

# Step 6: Display Summary of Clustering
unique_labels = set(labels_hdbscan)
n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
print(f"\nTotal clusters found: {n_clusters} (excluding outliers)")