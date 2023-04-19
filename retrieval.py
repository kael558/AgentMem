import numpy as np
from numpy.linalg import norm
from datetime import datetime

from utility import text_embed


def exponential_decay(t):
    if t == 0:
        return 9999999999
    return 0.99 ** t


def calculate_recency(memory_object):
    # Calculate recency of memory object
    # Recency is a value between 0 and 1 with a
    recency = exponential_decay((datetime.now() - memory_object.last_access_timestamp).total_seconds())
    return recency

def cosine_similarity(A, B):
    cosine = np.dot(A, B) / (norm(A) * norm(B))
    return cosine

def calculate_relevance(query, memory_object):
    # Calculate relevance of memory object
    # Relevance is a value between 0 and 1
    query_embed = text_embed(query)
    description_embed = text_embed(memory_object.nlp_description)

    relevance = cosine_similarity(query_embed, description_embed)
    return relevance


def get_score(query, memory_object):
    recency = calculate_recency(memory_object)
    relevance = calculate_relevance(query, memory_object)
    importance = memory_object.importance

    # Normalize scores to a value between 0 and 1
    max_score = max(recency, relevance, importance)
    min_score = min(recency, relevance, importance)
    diff = max_score - min_score
    if diff == 0:
        return 0

    alpha_recency, alpha_relevance, alpha_importance = 1, 1, 1

    return sum([alpha_recency * (recency - min_score) / diff,
                alpha_relevance * (relevance - min_score) / diff,
                alpha_importance * (importance - min_score) / diff])


def retrieval_function(memory_stream, query, n=3):
    scores = []

    for memory_object in memory_stream:
        score = get_score(query, memory_object)
        scores.append((score, memory_object))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:n]
