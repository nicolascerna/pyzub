import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyzub",
    version="0.1.0",
    author="Nicolás Cerna",
    author_email="nicolascerna@uc.cl",
    description="A small package for manipulating subtitles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicolascerna/pyzub",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'Click',
        'chardet',
        'tqdm',
    ]
    entry_points={
        'console_scripts': ['pyzub=pyzub.cli:main', ],
    },
)
