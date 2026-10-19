import os
import tempfile
import unittest
from unittest import mock

try:
    from mods2docs.parser import lmod
except ModuleNotFoundError as error:
    if error.name != "lupa":
        raise
    lmod = None


@unittest.skipIf(lmod is None, "lupa is not installed")
class LmodParserTests(unittest.TestCase):
    def test_lmod_version_comparison_does_not_discard_module(self):
        lua_content = '''
if convertToCanonical(LmodVersion()) >= convertToCanonical("8.6.3") then
    extensions("gmxapi/0.5.0a1")
end
whatis([==[Description: GROMACS molecular dynamics]==])
depends_on("foss/2025b")
depends_on("CUDA/12.9.1")
setenv("EBROOTGROMACS", "/opt/apps/GROMACS/2026.2")
setenv("EBVERSIONGROMACS", "2026.2")
'''
        with tempfile.NamedTemporaryFile(mode="w", suffix=".lua", delete=False) as module_file:
            module_file.write(lua_content)
            module_path = module_file.name

        self.addCleanup(os.unlink, module_path)
        with (
            mock.patch.object(lmod, "log_module_info"),
            mock.patch.object(lmod, "extract_installer", return_value=None),
        ):
            module_info, _creation_date, _installer = lmod.extract_lua_info(module_path)

        self.assertIsNotNone(module_info)
        self.assertEqual(module_info["EB Version"], "2026.2")
        self.assertEqual(module_info["Loaded Modules"], ["foss/2025b", "CUDA/12.9.1"])

    def test_execution_failure_falls_back_to_static_extraction(self):
        lua_content = '''
local unsupported_result = unknown_query() > another_unknown_query()
whatis([==[Description: Recoverable package]==])
depends_on("GCC/14.3.0")
setenv("EBROOTEXAMPLE", "/opt/apps/Example/1.0")
setenv("EBVERSIONEXAMPLE", "1.0")
'''
        with tempfile.NamedTemporaryFile(mode="w", suffix=".lua", delete=False) as module_file:
            module_file.write(lua_content)
            module_path = module_file.name

        self.addCleanup(os.unlink, module_path)
        with (
            mock.patch.object(lmod, "log_module_info"),
            mock.patch.object(lmod, "extract_installer", return_value=None),
            mock.patch.object(lmod.utils, "append_file"),
        ):
            module_info, _creation_date, _installer = lmod.extract_lua_info(module_path)

        self.assertIsNotNone(module_info)
        self.assertEqual(module_info["EB Version"], "1.0")
        self.assertEqual(module_info["Loaded Modules"], ["GCC/14.3.0"])


if __name__ == "__main__":
    unittest.main()
