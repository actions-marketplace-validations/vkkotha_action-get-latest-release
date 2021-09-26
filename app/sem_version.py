import re
from operator import attrgetter
from .to_string import to_string

@to_string
class SemVersion:
    versionRe = re.compile(r'^(?P<prefix>(\D*)?)(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

    def __init__(self, strVersion):
        self.version = strVersion
        matches = SemVersion.versionRe.search(strVersion)
        if matches:
            self.prefix = matches.group('prefix')
            self.major = int(matches.group('major'))
            self.minor = int(matches.group('minor'))
            self.patch = int(matches.group('patch'))
            self.prerelease = matches.group('prerelease')
            self.buildmetadata = matches.group('buildmetadata')
        else:
            raise ValueError(f"Can not process sem version string: '{strVersion}'")

    def baseVersion(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        if isinstance(other, SemVersion):
            return self.version == other.version
        return False

    @staticmethod
    def sort(items, reverse=False):
        return sorted(items, key=attrgetter('major', 'minor', 'patch', 'prerelease', 'buildmetadata'), reverse=reverse)