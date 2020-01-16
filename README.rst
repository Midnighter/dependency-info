==============================
Package Dependency Information
==============================

.. image:: https://img.shields.io/pypi/v/depinfo.svg
   :target: https://pypi.org/project/depinfo/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/depinfo.svg
   :target: https://pypi.org/project/dependency-info/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/depinfo.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: https://github.com/Midnighter/dependency-info/blob/master/.github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://img.shields.io/travis/Midnighter/dependency-info/master.svg?label=Travis%20CI
   :target: https://travis-ci.org/Midnighter/dependency-info
   :alt: Travis CI

.. image:: https://codecov.io/gh/Midnighter/dependency-info/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/dependency-info
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

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

If instead you want to access and modify the information, you can make use of
the underlying functions that return dictionaries that map package names to
their current versions. By default it will include common build packages such as
``pip``.

.. code-block:: python

    from depinfo import get_pkg_info
    help(get_pkg_info)

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

* Copyright © 2018-2020, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.
