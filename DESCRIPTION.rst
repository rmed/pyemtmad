pyemtmad
========

pyemtmad is a wrapper for the EMT API available at
http://opendata.emtmadrid.es/Servicios-web.

Quickstart
----------

Install with:

::

    pip install pyemtmad

Obtain credentials from the `EMT
website <http://opendata.emtmadrid.es/Formulario.aspx>`__ and
instantiate a ``Wrapper``:

.. code:: python

    from pyemtmad import Wrapper

    wrapper = Wrapper('MY_ID', 'MY_PASS')

    # wrapper.bus...
    # wrapper.geo...
    # wrapper.parking...

Documentation
-------------

Check the documentation online at http://pyemtmad.readthedocs.io or
build it from source using Sphinx from the ``doc/`` directory:

::

    make html
