import os
import re
from collections import defaultdict


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)

    def _tokenize(self, text):
        text = text.lower()
        return re.findall(r'\w+', text)

    def index_documents(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                    words = self._tokenize(content)

                    for word in words:
                        if filename not in self.index[word]:
                            self.index[word][filename] = 0
                        self.index[word][filename] += 1

    def boolean_search(self, query):
        tokens = query.lower().split()

        if not tokens:
            return {}

        result_set = None
        current_op = "AND"

        for token in tokens:
            if token in ["and", "or", "not"]:
                current_op = token.upper()
                continue

            docs = set(self.index.get(token, {}).keys())

            if result_set is None:
                result_set = docs
            else:
                if current_op == "AND":
                    result_set = result_set & docs
                elif current_op == "OR":
                    result_set = result_set | docs
                elif current_op == "NOT":
                    result_set = result_set - docs

        if not result_set:
            return {}

        return {doc: 1 for doc in result_set}
