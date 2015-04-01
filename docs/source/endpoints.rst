API endpoints
=============

Sikre is a REST type API, here is the list of all it's endpoints and required
methods.

Authentication
--------------

Categories
----------

Categories is the top level data that you can have, inside the categories you
can find the items and the services. An example of a category could be
"Facebook", in case you have more than one Facebook password or service or
for example "Google" and inside you store multiple items with your GMail accounts
and other services like Analytics, etc.

``GET`` ``/v1/categories``
    Return a list of all the category objects assigned or created to/for that
    user. The information returned is only the ``name`` and the ``id`` of the
    category.

    Example JSON::

        [
          {
            "id": 4,
            "name": "Category 1"
          },
          {
            "id": 5,
            "name": "Category 2"
          },
          {
            "id": 6,
            "name": "Category 3"
          }
        ]

``POST`` ``/v1/categories``
    Saves the information for a new category. The only data needed is the
    category ``name``.

    Example JSON::

        {
          "name": "Category 4"
        }

    The rest of the information is worked out through the ``JWT token`` sent in
    the header.

Specific categories
~~~~~~~~~~~~~~~~~~~

``GET`` ``/v1/categories/<id>``
    Return the information of a specific category, the result is the same as
    for the whole categories list, but only for one object.

    Example JSON::

        [
          {
            "id": 4,
            "name": "Category 1"
          },
        ]

``PUT`` ``/v1/categories/<id>``
    This method is used to edit an existing category. The UI retrieves the
    category and after the user modifies the content, we send back a ``PUT``
    request with the new information. The only data needed is the category
    ``name``.

    Example JSON::

        {
          "name": "Category 4-1"
        }

    The rest of the information is worked out through the JWT token sent in
    the header.

``DELETE`` ``/v1/categories/<id>``
    This method deletes a specified category **and all it's siblings**, that
    means, if the category contains items or services inside the items, everything
    will be deleted.

Items
-----

Services
--------

Generic
-------

Generic endpoints provide information about the API and also serve the purpose
of testing the API.
