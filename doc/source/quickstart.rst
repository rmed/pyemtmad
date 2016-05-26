Quickstart
==========

Installation
------------

**pyemtmad** can be installed directly from PyPI::

    pip install Flask-WaffleConf

Usage
-----

First, you need to obtain an ID and a key from the `EMT website
<http://opendata.emtmadrid.es/Formulario.aspx>`_. Once you have your
credentials, simply instantiate a ``Wrapper`` as follows:

.. code-block:: python

   from pyemtmad import Wrapper

   wrapper = Wrapper('MY_ID', 'MY_PASSWORD')


API endpoints are implemented in:

- :doc:`pyemtmad.api.bus`
- :doc:`pyemtmad.api.geo`
- :doc:`pyemtmad.api.parking`

The functions can be accessed directly from the wrapper through the ``bus``,
``geo`` and ``parking`` attributes of the object. For example:

.. code-block:: python

   from pyemtmad import Wrapper

   wrapper = Wrapper('MY_ID', 'MY_PASSWORD')

   # Bus API
   b = wrapper.bus.get_calendar(MY_ARGS)

   # Geo API
   g = wrapper.geo.get_arrive_stop(MY_ARGS)

   # Parking API
   p = wrapper.parking.detail_parking(MY_ARGS)


Check the :doc:`pyemtmad` for details on each method and their arguments.
