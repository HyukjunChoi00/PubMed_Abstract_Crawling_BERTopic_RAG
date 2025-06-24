#1 BERTopic
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Mecab
from bertopic import BERTopic
import pandas as pd

# Your file
docs = pd.read_csv("Pubmed_2021_2023.csv")
docc=docs["abstract"].astype(str).values.tolist()
from umap import UMAP

umap_model = UMAP(n_neighbors=15, n_components=6, metric='cosine', low_memory=False)
topic_model = BERTopic(umap_model=umap_model).fit(docc)
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

vectorizer_model = CountVectorizer(stop_words=["to","and","liposomes","of","was","lipid","is","be","publication","publishers",
                                              "bentham","copyright","doi","drug","we","delivery","as","cells","nanoparticles",
                                              "article","journal","for","are","by","can","retracts","submitting","authors","manuscripts",
                                              "editorial","plagiarism","permission","published","disclaimer","legal","forbidden","corrects",
                                              "apologizes","inconvenience","withdrawn","illustration","science","policy","table",
                                              "submitted","have","cell","if","readers","httpsbenthamsciencecomeditorialpoliciesmainphp","withdrawal",
                                              "yechezkel","barenholzs","using","results","elsewhere","strictly","study","treatment","on"])
from bertopic.representation import MaximalMarginalRelevance

# Hyperparmeter setting
representation_model = MaximalMarginalRelevance(diversity=0.1)
#topic_model = BERTopic(representation_model=representation_model)
model = BERTopic(vectorizer_model=vectorizer_model,ctfidf_model=ctfidf_model,representation_model=representation_model,
                 top_n_words=15,min_topic_size=35)
topics, probabilities = model.fit_transform(docc)

# Visualize
#model.get_topic_info()
model.visualize_topics()
##model.visualize_barchart()
