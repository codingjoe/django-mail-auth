============
Contributing
============

To install the development requirements simply run::

    python -m pip install -e '.[test]'

To run test suite run::

    python -m pytest

To build the documentation run::

    python -m sphinx -W -b spelling docs docs/_build

The sample app
==============

To run a full example — e.g. to debug frontend code – you can run::

    python -m pip install -e .
    python tests/testapp/manage.py migrate
    python tests/testapp/manage.py createsuperuser
    # You will be asked for the email address of your new superuser
    python tests/testapp/manage.py runserver

Next you can go to https://localhost:8000/admin/ and log in with your newly
created superuser.
