to build:

- make a folder named `python_utilities_build`.
- get source code.  Either:

    - clone this repository into that folder: `git clone https://github.com/jonathanmorgan/python_utilities"
    - or (DO THIS) grab the release source tar ball for the release you want to build.

- move the following files into `python_utilities_build`:

    - python_utilities/build/LICENSE
    - python_utilities/build/setup.py
    - python_utilities/README.md

- make sure you have `setuptools`, `wheel`, and `twine` packages installed in the Python environment you are using to build.
- in the `python_utilities_build` folder:

    - build: `python setup.py sdist bdist_wheel`
    - test upload to test.pypi.org: `python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
    - to install from test: `pip install --index-url https://test.pypi.org/simple/ python-utilities-jsm`
    - if all works OK, upload to pypi.org: `python3 -m twine upload dist/*`
    - install using pip and test: `pip install python-utilities-jsm`