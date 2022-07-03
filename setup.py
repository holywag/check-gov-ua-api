from setuptools import setup

setup(
    name='check_gov_ua',
    version='1.0',
    package_dir={'': 'src'},
    py_modules=['check_gov_ua'],
    requires=['requests'],
)
