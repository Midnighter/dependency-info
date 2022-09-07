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


Example
=======
The simplest way to display dependencies is to use the command line tool:

.. code-block:: console

    depinfo "your-package-name"

To print the dependencies of this package use (also try the ``--markdown`` option):

.. code-block:: console

    depinfo "depinfo"

.. code-block:: console

    Package Information
    -------------------
    depinfo 2.2.0

    Dependency Information
    ----------------------
    black               22.3.0
    importlib-metadata missing
    isort               5.10.1
    rich                12.4.4
    tox                 3.25.0

    Build Tools Information
    -----------------------
    pbr         5.9.0
    pip        22.1.2
    setuptools 62.3.2
    wheel      0.37.1

    Platform Information
    --------------------
    Linux   5.17.5-76051705-generic-x86_64
    CPython                         3.10.2

Alternatively you can use this package directly from Python

.. code-block:: python

    from depinfo.application import DisplayApplication

    DisplayApplication.run("depinfo")

Copyright
=========

* Copyright © 2018-2022, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.
