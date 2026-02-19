from inverted_index import InvertedIndex
from ranking import rank_tfidf
from tfidf import compute_tfidf
from trie import Trie


def main():
    engine = InvertedIndex()
    engine.index_documents("documents")

    # Count total unique documents
    total_docs = len(set(
        doc for word in engine.index.values() for doc in word
    ))

    tfidf_scores = compute_tfidf(engine.index, total_docs)

    # Build Trie
    trie = Trie()
    for word in engine.index.keys():
        trie.insert(word)

    print("Mini Search Engine Pro 🔍")
    print("Type 'exit' to quit.")
    print("Type 'auto <prefix>' for autocomplete.")
    print("Supports Boolean queries: AND / OR / NOT\n")

    while True:
        query = input("Search: ").strip()

        if query.lower() == "exit":
            break

        if query.lower().startswith("auto "):
            prefix = query.split(" ", 1)[1]
            suggestions = trie.autocomplete(prefix.lower())
            print("Suggestions:", suggestions[:5], "\n")
            continue

        results = engine.boolean_search(query)

        if not results:
            print("No results found.\n")
            continue

        query_words = [
            word for word in query.lower().split()
            if word not in ["and", "or", "not"]
        ]

        filtered_scores = {
            doc: tfidf_scores.get(doc, {})
            for doc in results.keys()
        }

        ranked = rank_tfidf(query_words, filtered_scores)

        if not ranked:
            print("No results found.\n")
            continue

        print("\nTop Results:")
        for doc, score in ranked:
            print(f"{doc} (TF-IDF score: {score:.4f})")
        print()


if __name__ == "__main__":
    main()
