#!/usr/bin/env python3

import os
import logging, sys
from github import Github
from app.sem_version import SemVersion

# Setup logging
root_log_level = getattr(logging, os.getenv('LOG_LEVEL_ROOT', 'INFO').upper(), logging.INFO)
app_log_level = getattr(logging, os.getenv('LOG_LEVEL_APP', 'INFO').upper(), logging.INFO)

logger = logging.getLogger( __name__ )
logging.basicConfig(stream=sys.stderr, level=root_log_level)
logger.setLevel(app_log_level)
print(f'Using: [root_log_level: { logging.getLevelName(logging.getLogger().getEffectiveLevel()) }, \
app_log_level: { logging.getLevelName(logger.getEffectiveLevel()) }]')

# Inputs
github_token = os.getenv('GITHUB_TOKEN', None)
github_repository = os.getenv('GITHUB_REPOSITORY')
branch = os.getenv('GITHUB_REF', 'main')
input_release_tag_prefix = os.getenv('INPUT_RELEASE_TAG_PREFIX', 'v')
input_scope = os.getenv('INPUT_SCOPE', 'branch')

def validateInputs():
    valid_scopes = ['all', 'branch']
    if (input_scope not in valid_scopes):
        raise ValueError(f'Invalid input: scope. Valid values {valid_scopes}')

def getSemanticTags(repo):
    tags = repo.get_tags()
    stags = {}
    for t in tags:
        # Index only tags matching semversion
        try:
            st = SemVersion(t.name)
            if (st.prefix == input_release_tag_prefix):
                stags[t.name] = { 'tag': t, 'sem_version': st }
        except Exception as e:
            logger.error(e)
    return stags

def printTags(tags):
    if (logger.isEnabledFor(logging.DEBUG)):
        logger.debug('Tags')
        for tag_name, tag_item in tags.items():
            t = tag_item['tag']
            version = tag_item['sem_version']
            logger.debug(f'{t.commit.sha[:8]} {tag_name} {version}')

def getSemanticReleases(repo, tags):
    releases = repo.get_releases()
    sem_releases = []
    sem_releases_idx = {}
    sem_releases_commit_idx = {}

    for r in releases:
        tag_info = tags.get(r.tag_name)
        if (tag_info is not None):
            tag = tag_info['tag']
            commit_sha = tag.commit.sha
            version = tag_info['sem_version']
            sem_releases.append(r)
            sem_releases_idx[r.tag_name] = { 'release': r, 'tag': tag, 'sem_version': version}
            sem_releases_commit_idx[commit_sha] = { 'release': r, 'tag': tag, 'sem_version': version}

    return { 'releases': sem_releases, 'releases_idx': sem_releases_idx, 'releases_commit_idx': sem_releases_commit_idx }

def printReleases(releases_info):
    if (logger.isEnabledFor(logging.DEBUG)):
        releases = releases_info['releases']
        releases_idx = releases_info['releases_idx']
        logger.debug('Releases')
        for r in releases:
            release_details = releases_idx[r.tag_name]
            logger.debug(f'{releaseToString(release_details)}')

def releaseToString(release_details):
    r = release_details['release']
    tag = release_details['tag']
    return f'Release(id: {r.id}, title: {r.title}, draft: {r.draft}, prerelease: {r.prerelease}, tag: {r.tag_name}, commit_sha: {tag.commit.sha[:8]})'

def getLatestRelease(repo, releases):
    commits = repo.get_commits(sha=branch)
    for c in commits:
        releases_commit_idx = releases['releases_commit_idx']
        release_details = releases_commit_idx.get(c.sha)
        if isValidRelease(release_details):
            return release_details

def isValidRelease(release_details):
    if (release_details == None):
        return False
    r = release_details['release']
    if (r.prerelease == False and r.draft == False):
        return True
    return False

def setOutputs(latest_release):
    if (latest_release is None):
        logger.info('Latest Release Not Found.')
        return

    logger.info(f'Latest Release Found: {releaseToString(latest_release)}')
    r = latest_release['release']
    tag = latest_release['tag']
    print(f'::set-output name=release_id::{r.id}')
    print(f'::set-output name=release_title::\'{r.title}\'')
    print(f'::set-output name=release_tag::{r.tag_name}')
    print(f'::set-output name=release_sha::{tag.commit.sha}')

def main():
    validateInputs()

    G = Github(github_token)
    repo = G.get_repo(github_repository)

    tags = getSemanticTags(repo)
    printTags(tags)
    releases = getSemanticReleases(repo, tags)
    printReleases(releases)
    latest_release = getLatestRelease(repo, releases)
    setOutputs(latest_release)

if __name__ == '__main__':
    main()