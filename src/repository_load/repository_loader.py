from typing import Callable
from langchain_community.document_loaders import GitLoader 
from pathlib import Path
import sys
from langchain_core.documents import Document
from git import Git

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.file_filter import file_filter

def repository_loader(clone_url:str, branch: str | None=None)-> list[Document]:
    """
    Clone a Git repository and load its files as LangChain Documents.

    The repository is cloned into the project's `repos/` directory if it
    does not already exist. Files are filtered using the configured
    `file_filter` function before being loaded.

    Args:
        clone_url (str):
            URL of the GitHub repository to clone and load.

        branch (str |None):
            Repository branch to load.
            In case of not entering, loads the default branch. 
            eg. 'master' or 'main'

    Returns:
        list[Document]:
            A list of LangChain Document objects representing the
            repository files that passed the file filter.
    """
    try:
        clone_url = clone_url.rstrip("/")

        repo_name = clone_url.split("/")[-1].replace(".git", "")

        if not clone_url.endswith(".git"):
            clone_url += ".git"

        project_root = Path(__file__).resolve().parent.parent.parent

        repos_dir = project_root / "repos"
        repos_dir.mkdir(exist_ok=True)
        repo_path = repos_dir / repo_name

        refs = Git().ls_remote(
            "--symref",
            clone_url,
            "HEAD"
        )

        default_branch = (
            refs.split("\n")[0]
            .split("refs/heads/")[1]
            .split()[0]
        )

        loader=GitLoader(
            repo_path=repo_path,
            clone_url=clone_url,
            file_filter=file_filter,
            branch=branch
        )
        if branch:
            loader.branch=branch
        docs=loader.load()
        return docs

    except GitCommandError as e:
        raise RuntimeError(
            f"Git operation failed. "
            f"Check whether branch '{branch}' exists and the repository URL is valid."
        ) from e

    except FileNotFoundError as e:
        raise RuntimeError(
            "Git executable not found. Make sure Git is installed and available in PATH."
        ) from e

    except Exception as e:
        raise RuntimeError(
            f"Unexpected error while loading repository '{clone_url}': {e}"
        ) from e

if __name__=='__main__':
    clone_url="https://github.com/gaurangagar/Feedloop"
    docs=repository_loader(clone_url)
    # for doc in docs:
    #     print(doc)
    print(f"Loaded {len(docs)} files")