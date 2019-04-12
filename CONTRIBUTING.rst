============
Contributing
============

To install the development requirements simply run::

    python setup.py develop

To run test suite run::

    python setup.py test

... and to run the entire test suite, simply use tox::

    pip install --upgrade tox
    tox

To build the documentation run::

    python setup.py build_sphinx
    open docs/_build/html/index.html
