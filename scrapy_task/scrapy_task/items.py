from dataclasses import dataclass


@dataclass
class GithubItem:
    _id: str
    name: str
    description: str
    link: str
    star: str
    fork: str
    watching: str
    commit: str
    release: str


@dataclass
class ReleaseInfo:
    version: str
    time: str
    changelog: str


@dataclass
class CommitInfo:
    author: str
    name: str
    datetime: str
