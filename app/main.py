import os
import logging, sys
from github import Github
from .sem_version import SemVersion

# Setup logging
root_log_level = getattr(logging, os.getenv('LOG_LEVEL_ROOT', 'INFO').upper(), logging.INFO)
app_log_level = getattr(logging, os.getenv('LOG_LEVEL_APP', 'INFO').upper(), logging.INFO)

logger = logging.getLogger( __name__ )
logging.basicConfig(stream=sys.stderr, level=root_log_level)
logger.setLevel(app_log_level)
print(f'Using: [root_log_level: { logging.getLevelName(logging.getLogger().getEffectiveLevel()) }, \
app_log_level: { logging.getLevelName(logger.getEffectiveLevel()) }]')

# Inputs
github_repository = os.getenv('GITHUB_REPOSITORY')
branch = os.getenv('GITHUB_REF', 'main')
github_token = os.getenv('INPUT_GITHUB_TOKEN', None)
release_tag_prefix = os.getenv('INPUT_RELEASE_TAG_PREFIX', 'v')
search_scope = os.getenv('INPUT_SEARCH_SCOPE', 'branch')
max_commits_to_scan = os.getenv('INPUT_MAX_COMMITS_TO_SCAN', '500')
commits_to_scan = 100

def validateInputs():
    valid_scopes = ['repo', 'branch']
    if (search_scope not in valid_scopes):
        raise ValueError(f'Invalid input: search_scope. Valid values {valid_scopes}')
    commits_to_scan = int(max_commits_to_scan)

def getSemanticTags(repo):
    tags = repo.get_tags()
    stags = {}
    for t in tags:
        # Index only tags matching semversion
        try:
            st = SemVersion(t.name)
            if (st.prefix == release_tag_prefix):
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

def getLatestReleaseForBranch(repo, releases):
    commits = repo.get_commits(sha=branch)
    cnt = 0
    for c in commits:
        ++cnt
        if (cnt > commits_to_scan):
            logger.warn(f'Max Commit scan threshold {commits_to_scan} reached. Please increase the limit.')
            break;
        releases_commit_idx = releases['releases_commit_idx']
        release_details = releases_commit_idx.get(c.sha)
        if isValidRelease(release_details):
            return release_details

def getLatestReleaseForRepo(repo, releases):
    releasesIdx = releases['releases_idx']
    releasesList = releasesIdx.values()
    semVersionList = [item['sem_version'] for item in releasesList if 'sem_version' in item]
    sortedVersions = SemVersion.sort(semVersionList, reverse=True)
    if (len(sortedVersions) > 0):
        maxVersion = sortedVersions[0]
        return releasesIdx.get(maxVersion.version)

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
    latest_release = None
    if (search_scope == "branch"):
        latest_release = getLatestReleaseForBranch(repo, releases)
    else:
        latest_release = getLatestReleaseForRepo(repo, releases)

    setOutputs(latest_release)

if __name__ == '__main__':
    main()