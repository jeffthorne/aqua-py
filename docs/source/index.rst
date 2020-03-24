.. aqua-py documentation master file, created by
   sphinx-quickstart on Tue Sept 17, 2019
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directives...



Welcome to Aqua-py
==================

A fantastic Python 3 client for Aqua's Container Security Platform.

|

Installation
------------

.. code-block:: python

   pip install aqua

|
| This project is an early stage effort and has a status of experimental. Questions, Comments, Feedback, Missing Calls, etc.
| Drop me a line @ jeff.thorne@aquasec.com


|
| Note: Requires Python 3.6 or higher due to reliance on Python's typing module and f strings.
|


Getting Started
---------------
Start by creating an Aqua object. This object represents the Aqua CSP API endpoint

.. code-block:: python

   from aqua import Aqua

   aqua = Aqua(id='administrator', password='password', host='mylo.uw.edu')

| Note: At this time there is no need to specify API version. The SDK does this on your behalf.
|

Example Usage
--------------
Please refer to the Endpoint api doc at :doc:`aqua.aqua` for current sdk api endpoint capabilities.

1. Authentication: `GithHub <https://github.com/aquasecurity/aqua-py/blob/master/examples/authentication.py/>`_.
2. Image Assurance: `GitHub <https://github.com/aquasecurity/aqua-py/blob/master/examples/image_assurance.py/>`_.

|
|

Use Cases
---------

Example use cases from the field.

1. Image profiling build task: `GitHub <https://github.com/jeffthorne/aqua_examples>`_
2. Create Enforcer Group: `GitHub <https://github.com/aquasecurity/aqua-py/blob/master/examples/create_enforcer_group.py/>`_.
3. k8s Admission controller: `GitHub <https://github.com/jeffthorne/rancher-admission-webhook>`_
4. Custom Excel Report: `GitHub <https://github.com/jeffthorne/aqua-reports>`_
5. Full image details: `GitHub <https://github.com/jeffthorne/datarequirements>`_


