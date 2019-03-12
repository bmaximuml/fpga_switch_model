from setuptools import setup

setup(
    name='fpga_switch_model',
    version='0.1',
    py_modules=['fpga_switch_model'],
    install_requires=[
        'Click',
        'logging'
    ],
    entry_points='''
        [console_scripts]
        fpga_switch_model=fpga_switch_model:cli
    ''',
)
