.. _gsl_bessemer:

GSL
===

.. sidebar:: GSL
   
   :Version: 2.6
   :URL: https://www.gnu.org/software/gsl/
   :Documentation: https://www.gnu.org/software/gsl/doc/html/index.html

The GNU Scientific Library (GSL) is a collection of routines for numerical computing. 
The routines have been written from scratch in C.  
See `here <https://www.gnu.org/software/gsl/doc/html/intro.html>`__ for the types of routines that the GSL provides.

Usage
-----

The GSL library can be loaded by running one of: ::

   module load GSL/2.6-GCC-8.3.0
   module load GSL/2.5-GCC-8.2.0-2.31.1

which will also load a particular :ref:`GCC <gcc_bessemer>`,
*or*: ::

   module load GSL/2.5-iccifort-2019.1.144-GCC-8.2.0-2.31.1

if you also want to activate or have already activated :ref:`icc/icpc/ifort <icc_ifort_bessemer>` 2019.1.

Example
-------

A example program that uses the GSL (taken from the GSL documentation):

.. code-block:: c

   #include <stdio.h>
   #include <stdlib.h>
   #include <gsl/gsl_sf_bessel.h>

   int main (void) {
     double x = 5.0;
     double y = gsl_sf_bessel_J0(x);

     printf("J0(%g) = %.18e\n", x, y);

     return EXIT_SUCCESS;
   }

Build this using:

.. code-block:: sh

   gcc -Wall -lgsl -lgslcblas -o test test.c  # OR
   icc -Wall -lgsl -lgslcblas -o test test.c 

Then run using:

.. code-block:: sh

    ./test

which should print the following (correct to double-precision accuracy): ::

    J0(5) = -1.775967713143382642e-01

NB generally, you may not need to compile using ``-lgslcblas`` depending on which GSL routines you are using.
