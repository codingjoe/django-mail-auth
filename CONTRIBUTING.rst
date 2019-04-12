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


The sample app
==============

To run a full example — e.g. to debug frontend code – you can run::

    python setup.py develop
    python tests/testapp/manage.py migrate
    python tests/testapp/manage.py createsuperuser
    # You will be asked for the email address of your new superuser
    python tests/testapp/manage.py runserver

Next you can go to https://localhost:8000/admin/ and log in with your newly
created superuser.
