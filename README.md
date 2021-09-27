## action-get-latest-release
**action-get-latest-release**: Gets the latest release info for the current branch from github.
The release tag output from this action can be used to generate release notes per branch using other release notes/change log generation plugins.

### Configuration

#### Inputs
|input |description|default|
|----- |-----------|-------|
|github_token|Git hub token. Use `${{ secrets.GITHUB_TOKEN }}` ||
|release_tag_prefix|Prefix for Server Version tags.|v|
|search_scope|Scope in which to search for releases.|branch|
Possible values for `search_scope` input
- *branch*: Looks for release on current branch commits. Release tied to the latest commit with Semantic release tag is used as the latest release.<br>
- *repo*: Version with the highest Semantic release tag is used across all branches. Time when the release is created is ignored.  

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
        uses: vkkotha/action-get-latest-release@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
      - name: Use Release Info
        run: |
          echo 'Latest release: ${{ steps.latest_release.outputs.release_tag }}'
```

## Contributing
### Submit code
- Fork Repository and Clone.
- Create feature branch and commit.
- push changes to Cloned repo.
- Create pull request and submit.
### Report Defects
- Submit new issues [Here](https://github.com/vkkotha/action-get-latest-release/issues/new)

## License
action-get-latest-release is provided under the [Apache License.](https://github.com/vkkotha/action-get-latest-release/blob/master/LICENSE)
