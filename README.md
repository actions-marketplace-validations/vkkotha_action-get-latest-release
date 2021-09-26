## action-get-latest-release
**action-get-latest-release** gets the latest release info for the current branch from github.
The release tag output from this action can be used to generate release notes per branch using other release notes/change log generation plugins.

### Configuration
#### Inputs
```yaml
inputs:
  release_tag_prefix:
    description: 'Prefix for Sem Version Tags'
    required: true
    default: 'v'
  search_scope:
    description: 'Search scope for searching for releases'
    required: true
    # Possible values [ 'all', 'branch' ]
    default: 'branch'
```
#### Outputs
```yaml
outputs:
  release_id:
    description: 'Github Release Id'
  release_tag:
    description: 'Release tag'
  release_title:
    description: 'Release title'
  release_sha:
    description: 'Release Commit sha'
```
### Usage

