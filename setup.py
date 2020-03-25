import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sameWidther",
    version="0.0.1",
    author="Jan Šindler",
    author_email="jansindl3r@gmail.com",
    maintainer="Jan Šindler",
    maintainer_email="jansindl3r@gmail.com",
    description="Get random words in given width based on a chosen font",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jansindl3r/sameWidther",
    # packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms=["Any"],
    python_requires='>=3.6',
    package_dir={'': 'Lib'},
    packages=setuptools.find_packages("Lib"),
    keywords='graphic design font typeface specimen typemedia',  # Optional
    entry_points={
		'console_scripts': [
			"sameWidther=sameWidther"
		]
	},
    cmdclass={
		"release": 'release',
	},
    install_requires=[
        "FontTools>=3.32.0",
        "defcon>=0.6.0",
    ]
)