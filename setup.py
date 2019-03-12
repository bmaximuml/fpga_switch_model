import os
import subprocess


from setuptools import setup, find_packages
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
    packages=find_packages(),
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

    # metadata to display on PyPI
    author="Benji Levine",
    author_email="b.levine@warwick.ac.uk",
    description="This is a Python application for modelling networking topologies containing " + \
                "some FPGA-based switches which will perform compute.",
    keywords="fpga switch",
    url="https://github.com/benjilev08/fpga_switch_model",
    cmdclass={'install': PreInstallCommand},
)
