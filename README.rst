==============================
Package Dependency Information
==============================

.. image:: https://img.shields.io/pypi/v/depinfo.svg
   :target: https://pypi.org/project/depinfo/
   :alt: PyPI

.. image:: https://travis-ci.org/Midnighter/dependency-info.svg?branch=master
   :target: https://travis-ci.org/Midnighter/dependency-info
   :alt: Travis CI

.. image:: https://codecov.io/gh/Midnighter/dependency-info/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/dependency-info
   :alt: Codecov

A utility Python package intended for other library packages. Provides a
function that when called with your package name, will print
platform and dependency information.

Install
=======

It's as simple as:

.. code-block:: console

    pip install depinfo

Usage
=====

The easiest way is to implement the following in your package somewhere.

.. code-block:: python

    from depinfo import print_dependencies

    def show_versions():
        print_dependencies("your-package-name")

That's all there is to it.

Example
=======

.. code-block:: python

    from depinfo import print_dependencies
    print_dependencies("depinfo")

.. code-block:: console

    System Information
    ==================
    OS                     Linux
    OS-release 4.4.0-122-generic
    Python                 3.6.5

    Package Versions
    ================
    pip        10.0.1
    pipdeptree 0.12.1
    setuptools 39.0.1
    wheel      0.31.0

Copyright
=========

* Copyright (c) 2018, Moritz E. Beber.
* Free software: `Apache Software License 2.0 <https://github.com/Midnighter/dependency-info/blob/master/LICENSE>`_
