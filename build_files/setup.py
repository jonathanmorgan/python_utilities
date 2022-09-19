import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-utilities-jsm", # Replace with your own username
    version="1.1.2",
    author="Jonathan Morgan",
    author_email="jonathan.morgan.007@gmail.com",
    description="Myriad python utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanmorgan/python_utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities"
    ],
    install_requires=[
        "bagit",
        "beautifulsoup4",
        "bleach",
        "cchardet",
        "chardet",
        "ipykernel",
        "openpyxl",
        "regex",
        "requests",
        "six",
        "w3lib"
    ],
    python_requires='>=3.6',
)