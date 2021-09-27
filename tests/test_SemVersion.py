import unittest
import sys

from app.sem_version import SemVersion

class TestSemVersion(unittest.TestCase):

    def test_semversion_simple_format(self):
        version = "1.2.3"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 3)

    def test_semversion_to_string(self):
        version = "v1.2.3"
        sv = SemVersion(version)

        self.assertEqual(str(sv), 'SemVersion(version=v1.2.3, prefix=v, major=1, minor=2, patch=3, prerelease=None, buildmetadata=None)')

    def test_invalid_semversion_should_error(self):
        version = "release-xyz"
        with self.assertRaises(ValueError) as context:
            sv = SemVersion(version)
            print(sv)

        self.assertIn(version, str(context.exception))

    def test_invalid_semversion_with_immediate_dots_should_error(self):
        version = "release1.."
        with self.assertRaises(ValueError) as context:
            sv = SemVersion(version)
            print(sv)

        self.assertIn(version, str(context.exception))

    def test_for_short_version_with_no_minor(self):
        version = "v0"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 0)
        self.assertEqual(sv.minor, 0)
        self.assertEqual(sv.patch, 0)

    def test_for_short_version_with_no_patch(self):
        version = "v1.2"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 0)

    def test_semversion_with_prerelease(self):
        version = "1.2.3-beta.0"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 3)
        self.assertEqual(sv.prerelease, "beta.0")

    def test_semversion_with_buildmetadata(self):
        version = "1.2.3+1234"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 3)
        self.assertEqual(sv.buildmetadata, "1234")

    def test_semversion_with_prerelease_and_buildmetadata(self):
        version = "1.2.3-beta.1.2+1234"
        sv = SemVersion(version)

        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 3)
        self.assertEqual(sv.prerelease, "beta.1.2")
        self.assertEqual(sv.buildmetadata, "1234")

    def test_semversion_with_prefix(self):
        version = "release.1.2.3-beta.1.2+1234"
        sv = SemVersion(version)

        self.assertEqual(sv.prefix, "release.")
        self.assertEqual(sv.major, 1)
        self.assertEqual(sv.minor, 2)
        self.assertEqual(sv.patch, 3)
        self.assertEqual(sv.prerelease, "beta.1.2")
        self.assertEqual(sv.buildmetadata, "1234")

    def test_semversion_baseVersion(self):
        version = "release.1.2.3-beta.1.2+1234"
        sv = SemVersion(version)

        self.assertEqual(sv.baseVersion(), "1.2.3")

    def test_semversion_equals(self):
        version = "release.1.2.3-beta.1.2+1234"
        sv1 = SemVersion(version)
        sv2 = SemVersion(version)

        self.assertTrue(sv1 == sv2)

    def test_semversion_equals_for_non_matching(self):
        version1 = "release.1.2.3-beta.1.2+1234"
        version2 = "1.2.3"
        sv1 = SemVersion(version1)
        sv2 = SemVersion(version2)

        self.assertTrue(sv1 != sv2)

    def test_semversion_sort(self):
        lst = [SemVersion('1.2.4'), SemVersion('2.1.2'), SemVersion('1.2.3'), SemVersion('2.0.4')]
        slst = SemVersion.sort(lst)

        self.assertEqual(slst[0].version, lst[2].version) # 1.2.3
        self.assertEqual(slst[1].version, lst[0].version) # 1.2.4
        self.assertEqual(slst[2].version, lst[3].version) # 2.0.4
        self.assertEqual(slst[3].version, lst[1].version) # 2.1.2

    def test_semversion_sort_reverse(self):
        lst = [SemVersion('1.2.4'), SemVersion('2.1.2'), SemVersion('1.2.3'), SemVersion('2.0.4')]
        slst = SemVersion.sort(lst, reverse=True)

        self.assertEqual(slst[0].version, lst[1].version) # 2.1.2
        self.assertEqual(slst[1].version, lst[3].version) # 2.0.4
        self.assertEqual(slst[2].version, lst[0].version) # 1.2.4
        self.assertEqual(slst[3].version, lst[2].version) # 1.2.3

    def test_semversion_sort_with_short_versions(self):
        lst = [SemVersion('1.2.4'), SemVersion('2.1.2'), SemVersion('v1'), SemVersion('1.2.3'), SemVersion('2.0.4'), SemVersion('2.1')]
        slst = SemVersion.sort(lst)

        self.assertEqual(slst[0].version, lst[2].version) # v1
        self.assertEqual(slst[1].version, lst[3].version) # 1.2.3
        self.assertEqual(slst[2].version, lst[0].version) # 1.2.4
        self.assertEqual(slst[3].version, lst[4].version) # 2.0.4
        self.assertEqual(slst[4].version, lst[5].version) # 2.1
        self.assertEqual(slst[5].version, lst[1].version) # 2.1.2

if __name__ == '__main__':
    unittest.main()