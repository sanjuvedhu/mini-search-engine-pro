import math


def compute_tfidf(index, total_docs):
    tfidf_scores = {}

    for word, doc_dict in index.items():
        df = len(doc_dict)

        # Improved smooth IDF formula
        idf = math.log((total_docs + 1) / (df + 1)) + 1

        for doc, tf in doc_dict.items():
            if doc not in tfidf_scores:
                tfidf_scores[doc] = {}

            tfidf_scores[doc][word] = tf * idf

    return tfidf_scores
