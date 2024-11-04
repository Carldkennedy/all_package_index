.. _cmake_bessemer:

CMake
=====

CMake is a build tool commonly used when compiling other libraries.

Usage
-----

CMake can be loaded with one of: ::

   module load CMake/3.15.3-GCCcore-8.3.0  # compatible with foss-2019b toolchain
   module load CMake/3.13.3-GCCcore-8.2.0  # compatible with foss-2019a toolchain
   module load CMake/3.12.1-GCCcore-7.3.0  # compatible with foss-2018b toolchain

CMake has a run-time dependency on ``libstdc++`` so
the cmake module files depend on and load particular versions of the :ref:`GCC compiler <gcc_bessemer>`,
plus versions of the ncurses, zlib, bzip2 and cURL libraries.

Usage of CMake often involves: 

1. Creating and ``cd``-ing into a dedicated build directory within a source tree then
2. Running something like ``cmake -DSOME_OPTION -DANOTHER_OPTION ..``
