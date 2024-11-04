.. _netcdf_bessemer:

netCDF
======

.. sidebar:: netCDF

   :URL: https://www.unidata.ucar.edu/software/netcdf/

"NetCDF (Network Common Data Form) is a set of interfaces for array-oriented data access and a freely distributed collection of data access libraries for C, Fortran, C++, Java, and other languages. The netCDF libraries support a machine-independent format for representing scientific data. Together, the interfaces, libraries, and format support the creation, access, and sharing of scientific data."

Usage
-----

To **load this library** plus

* the :ref:`gompi or iimpi toolchain<bessemer_eb_toolchains>`
* an :ref:`HDF5 library <hdf5_bessemer>`
* (and the zlib and Szip libraries)

run *one* of the following: ::

   module load netCDF/4.6.2-gompi-2019a
   module load netCDF/4.6.2-iimpi-2019a

To load the **Fortran bindings** for netCDF plus

* netCDF itself
* the :ref:`gompi or iimpi toolchain<bessemer_eb_toolchains>`
* an :ref:`HDF5 library <hdf5_bessemer>`
* (and the zlib and Szip libraries)

run *one* of the following: ::

   module load netCDF-Fortran/4.4.5-gompi-2019a
   module load netCDF-Fortran/4.4.5-iimpi-2019a

