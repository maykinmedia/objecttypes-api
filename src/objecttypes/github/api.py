import os.path
from typing import List

from django.conf import settings

from github import Commit, ContentFile, Github, NamedUser

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


def get_user() -> NamedUser:
    config = GithubConfig.get_solo()
    g = Github(config.token)
    return g.get_user()


def create_file(
    file_name,
    file_content,
    message=None,
) -> Commit.Commit:

    config = GithubConfig.get_solo()
    g = Github(config.token)
    repo = g.get_repo(config.repo)

    path = os.path.join(config.folder, file_name)
    message = (
        message
        or f"Automatically created when the object was exported in the {settings.PROJECT_NAME} application"
    )
    created = repo.create_file(path=path, message=message, content=file_content)

    return created["commit"]


def update_file(file_name, file_content, message=None) -> Commit.Commit:
    config = GithubConfig.get_solo()
    g = Github(config.token)
    repo = g.get_repo(config.repo)

    path = os.path.join(config.folder, file_name)
    message = (
        message
        or f"Automatically updated when the object was exported in the {settings.PROJECT_NAME} application"
    )
    contents = repo.get_contents(path)
    updated = repo.update_file(
        path=path, message=message, content=file_content, sha=contents.sha
    )
    return updated["commit"]
