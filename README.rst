.. image:: https://travis-ci.org/pedros/mtgdeck.svg?branch=master
   :target: https://travis-ci.org/pedros/mtgdeck

.. image:: https://ci.appveyor.com/api/projects/status/1afabyk0mdbrwsd7?svg=true
   :target: https://ci.appveyor.com/project/pedros/mtgdeck

mtgdeck
=======

MTG decklist decoder and encoder library and application

What is it?
-----------

``mtgdeck`` is both an application and a (Python 3) library for decoding and
encoding various decklist formats for Magic: The Gathering.


Usage
-----

::
   
   # Automatically determine input format in standard input
   # and encode using default encoder (text) to standard output
   mtgdeck < input.mws > output.txt

   # Decode a Cockatrice decklist and encode to OCTGN, specifying files
   mtgdeck -d cod -e octgn -i input.cod -i output.o8d
