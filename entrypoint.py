#!/usr/bin/env python3

import os
from github import Github
from app.sem_version import SemVersion

# Inputs
branch = os.getenv('branch')
github_token = os.getenv('github_token', None)

G = Github(github_token)
repo = G.get_repo('vkkotha/ticker-tracker')
releases = repo.get_releases()

tags = []
for r in releases:
    print(f'Release Title: {r.title}, Draft: {r.draft}, Prerelease: {r.prerelease}, tag: {r.tag_name}')
    try:
        semTag = SemVersion(r.tag_name)
        tags.append(semTag)
    except Exception:
        pass

print()

for t in SemVersion.sort(tags, True):
    print(t.version)