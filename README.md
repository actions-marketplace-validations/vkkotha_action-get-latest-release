## action-get-latest-release 
[![CI](https://github.com/vkkotha/action-get-latest-release/actions/workflows/ci.yaml/badge.svg)](https://github.com/vkkotha/action-get-latest-release/actions/workflows/ci.yaml) 
![GitHub release (latest by date)](https://img.shields.io/github/v/release/vkkotha/action-get-latest-release)
![GitHub pull requests](https://img.shields.io/github/issues-pr/vkkotha/action-get-latest-release)
[![GitHub Issues](https://img.shields.io/github/issues/vkkotha/action-get-latest-release.svg)](https://github.com/vkkotha/action-get-latest-release/issues)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

Gets the latest release info for the current branch from github.
The release tag output from this action can be used to generate release notes per branch using other release notes/change log generation plugins.

### Configuration

#### Inputs
|input |description|default|
|----- |-----------|-------|
|github_token|Git hub token. Use `${{ secrets.GITHUB_TOKEN }}` ||
|release_tag_prefix|Prefix for Server Version tags.|v|
|search_scope|Scope in which to search for releases.|branch|
|max_commits_to_scan|Mac commits to walk before giving up finding the release|500|

Possible values for `search_scope` input
- *branch*: Looks for release on current branch commits. Release tied to the latest commit with Semantic release tag is used as the latest release.<br>
- *repo*: Version with the highest Semantic release tag is used across all branches. Time when the release is created is ignored.  

> **_NOTE:_** `max_commits_to_scan` sets the threshold on how many commits your can iterate before giving up finding the release on the branch. 
> github api rate limits may block you from doing too many requests, specially if you scan public repos with no github_token.
 
#### Outputs
- `release_id` - Github release Id
- `release_tag` - Release tag
- `release_title` - Release title
- `release_sha` - Release Commit sha

### Usage
```yaml
on:
  push:
    branches:
      - main
      - master
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Get Latest Release
        id: latest_release
        uses: vkkotha/action-get-latest-release@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
      - name: Use Release Info
        run: |
          echo 'Latest release: ${{ steps.latest_release.outputs.release_tag }}'
```

## Contributing
### Development
You can use python 3.9 locally to test and run the action.
All you need to do is set INPUT_GITHUB_TOKEN to your github PAC and run ./entrypoint.sh
#### Developing in docker container.
You can build a container with volume mounting to this code and run your code and tests with in the container.
To Build docker image run<br>
```sh
$ docker build -t action-get-latest-release-test \
    --build-arg requirements=requirements_test.txt .
```
Then run a container in shell mode with
```sh
$ docker run -it --rm --entrypoint sh --workdir=/github/workspace \
    -v $(pwd):/github/workspace action-get-latest-release-test
```
Once your are inside the container set up the following Environment variables
```sh
$ export GITHUB_REPOSITORY=<test repo>
$ export GITHUB_REF=[main | master | <your branch>]
$ export INPUT_GITHUB_TOKEN=<github PAC>
```

You can run the action by running ```/entrypoint.sh``` inside container. 

Running Unit tests
```sh
$ pytest --cache-clear --cov --cov-report=html tests/
```
Your coverage report will be in `htmlcov` folder
 
### Submit code
- Fork Repository and Clone.
- Create feature branch and commit.
- push changes to Cloned repo.
- Create pull request and submit.
### Report Defects
- Submit new issues [Here](https://github.com/vkkotha/action-get-latest-release/issues/new)

## Credits
- [github-tag-action](https://github.com/anothrNick/github-tag-action)
- [release-changelog-builder-action](https://github.com/mikepenz/release-changelog-builder-action)
- [action-bumper](https://github.com/haya14busa/action-bumpr)
- [actions-github-release](https://github.com/rez0n/actions-github-release)

## License
action-get-latest-release is provided under the [Apache License.](https://github.com/vkkotha/action-get-latest-release/blob/master/LICENSE)
