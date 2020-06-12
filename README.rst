drf-hmac-auth
======================================

|build-status-image| |pypi-version|

Overview
--------

An HMAC-token authentication's package. No need refresh token manually by a timer, with HMAC-algorithm user cannot change a timestamp from the server. And the server can check this timestamp from the client for an expiring.

Requirements
------------

-  Python (2.7, 3.3, 3.4)
-  Django (1.6, 1.7, 1.8)
-  Django REST Framework (2.4, 3.0, 3.1)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install drf-hmac-auth

Move to project folder and add 'hmac_auth' into INSTALLED_APPS in settings.py

.. code:: python

    INSTALLED_APPS = [
        ...
        'hmac_auth',
        ...
    ]

Make and run migrations

.. code:: bash

    $ python manage.py makemigrations hmac_auth
    $ python manage.py migrate

Set names of HTTP headers, a hash function's name (from hashlib.algorithms_available) and time of token's living in settings.py or leave it for this default values:

.. code:: python

    from hmac_auth.HMACToken import TokenPeriod

    HMAC_LOGIN_HEADER = 'HMAC-Login'
    HMAC_TOKEN_HEADER = 'HMAC-Token' 
    HMAC_TIMES_HEADER = 'HMAC-Times' 
    HMAC_HASH_FUNC = 'md5'
    HMAC_PERIOD = TokenPeriod.day # TokenPeriod.minute, hour, day, week, month, year also avaiable
    # You can also change a period like 'TokenPeriod.hour * 2.'

Example
-------

Create and return user's token

.. code:: python

    from hmac_auth.serializers import TokenSerializer

    ...

    class TokenView(APIView):
        def get(self, request, format=None):
            ...
            # user is an User model object
            token = TokenSerializer(user=user)
            if not token.is_valid():
                return Response(token.errors)
            return Response(token.data)

Check token and timing before access

.. code:: python

    from hmac_auth.permissions import TokenPermission
    
    ...

    class Perm(APIView):
    
        permission_classes = [TokenPermission]

    #some methods...

Example of HTTP headers

.. code:: yaml

    HMAC-Login: user
    HMAC-Times: 1591969217
    HMAC-Token: 4d56007c1836d4a01f362f3206168308f9cd994f9d8acfddf3600a8738bec00d


Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/VasyaSmolyar/drf-hmac-auth.svg?branch=master
   :target: http://travis-ci.org/VasyaSmolyar/drf-hmac-auth?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-hmac-auth.svg
   :target: https://pypi.python.org/pypi/drf-hmac-auth
