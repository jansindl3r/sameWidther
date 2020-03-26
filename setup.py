# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
	long_description = readme.read()

with open("requirements.txt", "r", encoding="utf-8") as requirements_in:
    requirements = requirements_in.read().splitlines()

setup(
    name='sameWidther',
    version='0.0.4',
    description='Gets random words of the same width for given font',
    keywords="font typography graphicdesign specimen width word",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jansindl3r/sameWidther',
    author='Jan Šindler',
    author_email='jansindl3r@gmail.com',
    license='MIT',
    package_dir={"": "Lib"},
    packages=[".", ".databases"],
    package_data={
        ".databases": ["*.json"],
    },
    entry_points={
        "console_scripts": [
            "sameWidther = sameWidther:main",
        ]
    },
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=requirements
    )
