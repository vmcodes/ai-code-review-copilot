import os
import shutil
from git import Repo


def clone_repo(repo_url):
    base_path = "repos"
    repo_name = repo_url.rstrip("/").split("/")[-1]
    clone_path = os.path.join(base_path, repo_name)

    # 🔥 Delete old repo if exists
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    # Ensure base directory exists
    os.makedirs(base_path, exist_ok=True)

    # Clone fresh repo
    Repo.clone_from(repo_url, clone_path)

    return clone_path