# Contributing

To run test suite run:

```console
uv run pytest
```

To build the documentation run:

```
uv run mkdocs serve
```

## The sample app

To run a full example --- e.g. to debug frontend code -- you can run:

```
uv run tests/manage.py migrate
uv run tests/manage.py createsuperuser
# You will be asked for the email address of your new superuser
uv run tests/manage.py runserver
```

Next you can go to <https://localhost:8000/admin/> and log in with your
newly created superuser.
