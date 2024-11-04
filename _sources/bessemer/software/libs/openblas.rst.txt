.. _openblas_bessemer:

OpenBLAS
========

.. sidebar:: OpenBLAS
   
   :URL: https://www.openblas.net/
   :Documentation: https://github.com/xianyi/OpenBLAS/wiki/User-Manual

OpenBLAS is one of the :ref:`BLAS <blas_bessemer>` implementations installed on Bessemer.
It also provides some optimised LAPACK routines.

Usage
-----

OpenBLAS can be activated using one of: ::

   module load OpenBLAS/0.3.7-GCC-8.3.0  # foss-2019b toolchain
   module load OpenBLAS/0.3.5-GCC-8.2.0-2.31.1  # foss-2019a toolchain
   module load OpenBLAS/0.3.1-GCC-7.3.0-2.30  # foss-2018b toolchain

which also loads a version of the :ref:`GCC <gcc_bessemer>` compiler.
