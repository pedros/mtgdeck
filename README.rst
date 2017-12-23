.. image:: https://travis-ci.org/pedros/mtgdeck.svg?branch=master
   :target: https://travis-ci.org/pedros/mtgdeck
   :alt: Linux builds passing

.. image:: https://ci.appveyor.com/api/projects/status/1afabyk0mdbrwsd7?svg=true
   :target: https://ci.appveyor.com/project/pedros/mtgdeck
   :alt: Windows builds passing

.. image:: https://codecov.io/gh/pedros/mtgdeck/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pedros/mtgdeck
   :alt: Coverage

.. image:: https://api.codacy.com/project/badge/Grade/724c2300463b4f639bf406e1bfe1fe10
   :target: https://www.codacy.com/app/pedros/mtgdeck?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pedros/mtgdeck&amp;utm_campaign=Badge_Grade
   :alt: Grade

.. image:: https://api.codeclimate.com/v1/badges/67254f9c83a1eecb0598/maintainability
   :target: https://codeclimate.com/github/pedros/mtgdeck/maintainability
   :alt: Maintainability

.. image:: http://img.shields.io/pypi/v/mtgdeck.svg
   :target: https://pypi.python.org/pypi/mtgdeck
   :alt: PyPI version 

mtgdeck
=======

MTG decklist decoder and encoder library and application

What is it?
-----------

``mtgdeck`` is an application and library for decoding and encoding various
decklist formats for Magic: The Gathering.

Usage
-----

Automatically determine input format in standard input and encode using default
encoder (text) to standard output:

.. code:: bash

   mtgdeck < input.mws > output.txt

The same as above, but from Python:

.. code-block:: python

   import sys
   import mtgdeck
   mtgdeck.dump(mtgdeck.load(sys.stdin), sys.stdout)

Decode a Cockatrice decklist and encode to OCTGN, specifying files:

.. code:: bash

   mtgdeck -d cod -e octgn -i input.cod -o output.o8d

And in Python:

.. code-block:: python

   import mtgdeck
   src = open('input.cod')
   target = open('output.o8d', 'w')
   decklist = mtgdeck.load(src, cls=mtgdeck.CockatriceDecoder)
   mtgdeck.dump(decklist, target, cls=mtgdeck.OCTGNEncoder)

Formats
-------

``mtgdeck`` currently supports the following formats:

:Magic online:
   ``text`` (``.txt`` and ``.dec``)
:Magic Workstation:
   ``mws`` (``.mwDeck``)
:OCTGN:
   ``o8d`` (``.o8d``)
:Cockatrice:
   ``cod`` (``.cod``)

The default decoder is ``auto``: it tries to infer the correct decklist format.
The default encoder is ``text``.

Installation
------------

.. code-block:: bash

   pip install mtgdeck
   mtgdeck --help  # or python -m mtgdeck --help

Contributing
------------

See the `Contribution guidelines <CONTRIBUTING.rst>`_ file.
