import os
import tempfile
import unittest
from unittest import mock

from mods2docs import config
from mods2docs.writer import rest


class RestWriterTests(unittest.TestCase):
    def test_extract_url_handles_empty_and_valid_values(self):
        self.assertEqual(rest.extract_url(["URL:"]), "N/A")
        self.assertEqual(
            rest.extract_url(["Homepage: https://example.test", "URL: https://example.test/path"]),
            "https://example.test/path",
        )

    def test_package_failure_does_not_prevent_index_links_from_being_written(self):
        with tempfile.TemporaryDirectory() as directory:
            stacks_dir = os.path.join(directory, "stacks")
            imports_dir = os.path.join(directory, "imports")
            custom_dir = os.path.join(directory, "custom")
            os.makedirs(imports_dir)
            os.makedirs(custom_dir)

            package_ref = {"Broken": "Tools", "Working": "Tools"}
            package_infos = {"icelake": {}}
            latest_version_info = {
                f"Tools|{package}": {
                    "icelake": ({"Loaded Modules": []}, "2026-01-01", None)
                }
                for package in package_ref
            }

            def fail_for_broken(_category_dir, _category, package, _output_dir):
                if package == "Broken":
                    raise ValueError("malformed package")

            with (
                mock.patch.object(config, "STACKS_DIR", stacks_dir),
                mock.patch.object(config, "IMPORTS_DIR", imports_dir),
                mock.patch.object(config, "CUSTOM_DIR", custom_dir),
                mock.patch.object(config, "main_log_file", os.path.join(directory, "writer.log")),
                mock.patch.object(rest, "write_package_file", side_effect=fail_for_broken),
                mock.patch.object(rest, "write_ml_file"),
                mock.patch.object(rest, "write_description_file"),
                mock.patch.object(rest, "write_sidebar_file"),
                mock.patch.object(rest, "write_installation_file"),
                mock.patch.object(rest, "write_custom_file"),
                mock.patch.object(rest, "write_dependencies"),
            ):
                rest.write_all_files(
                    "Test stack",
                    "test-stack",
                    package_infos,
                    package_ref,
                    latest_version_info,
                )

            index_path = os.path.join(stacks_dir, "test-stack", "All", "index.rst")
            with open(index_path) as index_file:
                index_content = index_file.read()

            self.assertIn("* :ref:`Working <working-tools-test-stack>`", index_content)
            self.assertNotIn("* :ref:`Broken <broken-tools-test-stack>`", index_content)


if __name__ == "__main__":
    unittest.main()
