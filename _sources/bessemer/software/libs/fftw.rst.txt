.. _fftw_bessemer:

fftw
====

.. sidebar:: fftw

   :Latest version: 3.3.8
   :URL: https://www.fftw.org/

FFTW is a C subroutine library for
computing the discrete Fourier transform (DFT)
in one or more dimensions,
of arbitrary input size,
and of both real and complex data
(as well as of even/odd data,
i.e. the discrete cosine/sine transforms or DCT/DST).

Usage
-----
To make this library available, run one the following: ::

   module load FFTW/3.3.8-gompi-2019b
   module load FFTW/3.3.8-gompi-2019a
   module load FFTW/3.3.8-gompi-2018b
   module load FFTW/3.3.8-gompic-2019b
   module load FFTW/3.3.8-gompic-2019a
   module load FFTW/3.3.8-intel-2019a

- `gompi` versions are a subset of the :ref:`foss toolchain <bessemer_eb_toolchains>`
  and also load GCC and OpenMPI
- `gompic` versions are a subset of the :ref:`fosscuda toolchain <bessemer_eb_toolchains>`
  and also load GCC, OpenMPI and CUDA.
- `intel` versions use an ``intel`` toolchain and load the Intel compilers and Intel MPI.
