import os
import subprocess


from setuptools import setup
from setuptools.command.install import install


class PreInstallCommand(install):
    """Provides a wrapper to install mininet when the package is installed"""

    def run(self):
        # Run this first so the install stops if it fails
        self._install_mininet()
        # Run the standard install
        install.run(self)

    def _install_mininet(self):
        subprocess.call('mininet/util/install.sh -nfv', shell=True)
        if 'mininet/mininet' not in os.environ['PATH']:
            os.environ['PATH'] = os.environ['PATH'] + ':' + \
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'mininet', 'mininet')


setup(
    name='fpga_switch_model',
    version='0.1',
    py_modules=['fpga_switch_model'],
    install_requires=[
        'Click',
        'logging',
        'numpy'
    ],
    entry_points='''
        [console_scripts]
        fpga_switch_model=fpga_switch_model:cli
    ''',
    cmdclass={'install': PreInstallCommand},
)
