from setuptools import setup

setup(
    name='sameWidther',
    version='0.1',
    description='Gets random words of the same width for given font',
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
    zip_safe=False)
