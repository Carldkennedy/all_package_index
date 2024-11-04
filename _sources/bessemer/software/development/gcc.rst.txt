.. _gcc_bessemer:

GNU Compiler Collection (gcc)
=============================

The GNU Compiler Collection (gcc) is a widely used, free collection of compilers
for C (gcc), C++ (g++) and Fortran (gfortran).

It is possible to switch versions of the gcc compiler suite using modules.
After connecting to Bessemer,  start an interactive sessson: :: 

   srun --pty bash -i

then choose the version of the compiler you wish to use
by running *one* of the following lines: ::

   module load GCC/8.3.0  # part of the foss-2019b toolchain
   module load GCC/8.2.0-2.31.1  # part of the foss-2019a toolchain
   module load GCC/7.3.0-2.30  # part of the foss-2018b toolchain

Confirm that you've loaded the version of gcc you wanted using ``gcc -v``.

Language support
----------------

* Which version(s) of GCC support which features of the `C99 <https://gcc.gnu.org/c99status.html>`__ and `C11 <https://gcc.gnu.org/wiki/C11Status>`__ standards?
* `Which version(s) of GCC support which features of the C++98, C++11, C++14 and C++17 standards? <https://gcc.gnu.org/projects/cxx-status.html>`__

Documentation
-------------

man pages are available on the system.
Once you have loaded the required version of `gcc`, type ::

    man gcc

* `What's new in the gcc version 8 series? <https://gcc.gnu.org/gcc-8/changes.html>`__
