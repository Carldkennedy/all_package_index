import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.work = Path(directory.name)
        for name in ('run-hpc-rocket.sh', 'sync_stacks.sh'):
            shutil.copy2(ROOT / name, self.work / name)
        (self.work / 'mods2docs').mkdir()
        shutil.copy2(ROOT / 'mods2docs/config.yml', self.work / 'mods2docs/config.yml')
        (self.work / 'config.env').write_text(
            'STACKS_DIR=stanage/software/stacks\n'
            'IMPORTS_DIR=referenceinfo/imports\n'
            'DATA_DIR=data\n'
            'REPO_DIR=docs-checkout\n'
        )
        for name in ('stanage', 'referenceinfo', 'data', 'bin'):
            (self.work / name).mkdir()
        for name in ('stanage/previous.rst', 'referenceinfo/previous.rst',
                     'data/collected-data.pkl'):
            (self.work / name).write_text('previous run')
        self.stub('envsubst', 'cat')
        self.stub('python', 'touch pipeline-ran')
        self.stub('git', 'touch git-ran')
        self.stub('rsync', 'touch sync-ran')

    def stub(self, name, body):
        path = self.work / 'bin' / name
        path.write_text('#!/bin/bash\n' + body + '\n')
        path.chmod(0o755)

    def run_script(self, name, *args):
        env = dict(os.environ, PATH=str(self.work / 'bin') + ':' + os.environ['PATH'])
        return subprocess.run(['bash', name, *args], cwd=self.work, env=env,
                              capture_output=True, text=True)

    def assert_previous_output_preserved(self):
        for name in ('stanage/previous.rst', 'referenceinfo/previous.rst',
                     'data/collected-data.pkl'):
            self.assertEqual((self.work / name).read_text(), 'previous run')
        for name in ('pipeline-ran', 'git-ran', 'sync-ran', 'data/backups'):
            self.assertFalse((self.work / name).exists(), name)

    def test_remote_failure_stops_generation_and_preserves_output(self):
        self.stub('hpc-rocket', 'exit 23')
        result = self.run_script('run-hpc-rocket.sh')
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertIn('documentation generation stopped', result.stderr)
        self.assert_previous_output_preserved()

    def test_remote_failure_stops_outer_sync(self):
        self.stub('hpc-rocket', 'exit 23')
        result = self.run_script('sync_stacks.sh', '--rocket', '--push')
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assert_previous_output_preserved()

    def test_success_backs_up_returned_data_and_runs_writer(self):
        self.stub('hpc-rocket', "printf 'fresh data' > data/collected-data.pkl")
        result = self.run_script('run-hpc-rocket.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.work / 'pipeline-ran').exists())
        backups = list((self.work / 'data/backups').glob('*.bk'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'fresh data')

    def test_writer_failure_is_reported(self):
        self.stub('hpc-rocket', 'exit 0')
        self.stub('python', 'exit 17')
        result = self.run_script('sync_stacks.sh', '--rocket', '--push')
        self.assertEqual(result.returncode, 17, result.stderr)
        self.assertFalse((self.work / 'git-ran').exists())
        self.assertFalse((self.work / 'sync-ran').exists())


if __name__ == '__main__':
    unittest.main()
