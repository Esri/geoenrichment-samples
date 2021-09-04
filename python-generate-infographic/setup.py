from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='generate_infographic',
    package_dir={"": "src"},
    packages=find_packages('src'),
    version='0.0.0',
    description='Example for generating Esri Infogrpahics using Python.',
    long_description=long_description,
    author='Joel McCune',
    license='Apache 2.0',
)
