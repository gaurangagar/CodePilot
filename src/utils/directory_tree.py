from collections import defaultdict
from langchain_core.documents import Document

def docs_to_tree(docs:list[Document]):
    """
    Convert LangChain documents into a directory tree string.

    Args:
        docs: List of Document objects containing metadata["file_path"]

    Returns:
        str: Formatted tree structure
    """

    def tree():
        return defaultdict(tree)

    root = tree()

    # Build nested dictionary
    for doc in docs:
        path = doc.metadata["file_path"]
        parts = path.replace("\\", "/").split("/")

        current = root
        for part in parts:
            current = current[part]

    lines = []

    def build_tree(node, prefix=""):
        items = sorted(node.keys())

        for i, key in enumerate(items):
            is_last = i == len(items) - 1

            lines.append(
                prefix + ("└── " if is_last else "├── ") + key
            )

            extension = "    " if is_last else "│   "
            build_tree(node[key], prefix + extension)

    build_tree(root)

    return "\n".join(lines)