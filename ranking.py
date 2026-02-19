import heapq


def rank_tfidf(query_words, tfidf_scores, top_k=3):
    scores = {}

    for doc, word_scores in tfidf_scores.items():
        total_score = 0

        for word in query_words:
            if word in word_scores:
                total_score += word_scores[word]

        if total_score > 0:
            scores[doc] = total_score

    heap = []
    for doc, score in scores.items():
        heapq.heappush(heap, (-score, doc))

    ranked = []
    while heap and len(ranked) < top_k:
        score, doc = heapq.heappop(heap)
        ranked.append((doc, -score))

    return ranked
