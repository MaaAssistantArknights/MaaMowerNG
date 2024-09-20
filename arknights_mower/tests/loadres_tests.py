import unittest

from arknights_mower.utils import path
from arknights_mower.utils.image import res2path
from arknights_mower.utils.path import get_path

internal_dir = get_path("@install")
install_dir = get_path("@install")


class TestLogicExpression(unittest.TestCase):
    def test_single(self):
        res = res2path("infra_overview")
        relative_path = str(res.relative_to(internal_dir))
        self.assertEqual(relative_path, "arknights_mower/resources/infra_overview.png")

    def test_single_hot(self):
        res = res2path("@hot/inudi/banner")
        relative_path = str(res.relative_to(install_dir))
        self.assertEqual(relative_path, "tmp/hot_update/inudi/banner.png")

    def test_single_jpg(self):
        res = res2path("@hot/inudi/banner.jpg")
        relative_path = str(res.relative_to(install_dir))
        self.assertEqual(relative_path, "tmp/hot_update/inudi/banner.jpg")

    def test_multi(self):
        path.global_space = "/test/path"
        res = res2path("infra_overview")
        relative_path = str(res.relative_to(internal_dir))
        self.assertEqual(relative_path, "arknights_mower/resources/infra_overview.png")

    def test_multi_hot(self):
        path.global_space = "/test/path"
        res = res2path("@hot/inudi/banner")
        relative_path = str(res.relative_to(install_dir))
        self.assertEqual(relative_path, "tmp/hot_update/inudi/banner.png")


if __name__ == "__main__":
    unittest.main()
