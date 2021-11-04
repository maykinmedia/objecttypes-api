from typing import List

from github import Commit, ContentFile, Github

from .models import GithubConfig


def get_files_in_folder() -> List[ContentFile.ContentFile]:
    config = GithubConfig.get_solo()
    g = Github(config.token)
    repo = g.get_repo(config.repo)

    files = [
        content
        for content in repo.get_contents(config.folder)
        if content.type == "file"
    ]
    if config.only_json:
        files = [file for file in files if file.name.lower().endswith(".json")]

    return files


def get_last_commit_for_file(file_path: str) -> Commit.Commit:
    config = GithubConfig.get_solo()
    g = Github(config.token)
    repo = g.get_repo(config.repo)

    commits = repo.get_commits(path=file_path)
    return commits[0]
