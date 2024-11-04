.. _lapack_bessemer:

LAPACK
======
LAPACK is written in Fortran 90 and provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems. The associated matrix factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are also provided, as are related computations such as reordering of the Schur factorizations and estimating condition numbers. Dense and banded matrices are handled, but not general sparse matrices. In all areas, similar functionality is provided for real and complex matrices, in both single and double precision.

Usage
-----
LAPACK is available via the following module command ::

    module load LAPACK/3.8.0-GCC-7.3.0-2.30

Installation notes
------------------
This section is primarily for administrators of the system. LAPACK has been installed using the default Easybuild config files.

Build logs and test reports can be found in ``$EBROOTLAPACK/easybuild`` with a given module loaded.
