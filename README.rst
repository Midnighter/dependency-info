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

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
   :target: .github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://github.com/Midnighter/dependency-info/workflows/CI-CD/badge.svg
   :target: https://github.com/Midnighter/dependency-info/workflows/CI-CD
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/Midnighter/dependency-info/branch/stable/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/dependency-info
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style Black

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
    setuptools 39.0.1
    wheel      0.31.0

Copyright
=========

* Copyright © 2018-2020, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.
