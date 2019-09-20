.. aqua-py documentation master file, created by
   sphinx-quickstart on Tue Sept 17, 2019
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directives...



Welcome to Aqua-py
===============

A fantastic Python 3 client for Aqua's Container Security Platform..


Installation
------------

.. code-block:: python

   pip install aqua

| This project is an early stage effort and has a status of experimental. Questions, Comments, Feedback, Missing Calls, etc.
| Drop me a line @ jthorne@u.washington.edu


|
| Note: Requires Python 3.6 or higher due to reliance on Python's typing module and f strings.
|


Getting Started
---------------
Start by creating an Aqua object. This object represents the Aqua CSP API endpoint

.. code-block:: python

   from aqua import Aqua

   aqua = Aqua(id='username', password='password', host='host', port='port', using_ssl=True)



Example Usage
--------------
Please refer to the Endpoint api doc at :doc:`aqua.aqua` for current sdk api endpoint capabilities.




Use Cases
---------

Examples of customer use cases in the field.

1. Image profiling build task: `Github <https://github.com/jeffthorne/aqua_examples>`_
