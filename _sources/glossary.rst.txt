.. _glossary:

Glossary of Terms
=================
The worlds of scientific and high performance computing are full of technical
jargon that can seem daunting to newcomers. This glossary attempts to explain
some of the most common terms as quickly as possible.

.. glossary::

    HPC
        'High Performance Computing'. The exact definition of this term is
        sometimes a subject of great debate but for the purposes of our
        services you can think of it as 'Anything that requires more resources
        than a typical high-spec desktop or laptop PC'.

    GPU
        Acronymn for Graphics Processing Unit.

    SGE 
        Acronymn for Sun Grid Engine.

    Sun Grid Engine
        The Sun Grid Engine is the software that controls and allocates
        resources on the system. There are many variants of 'Sun Grid Engine'
        in use worldwide and the variant in use at Sheffield is the 
        `Son of Grid Engine <https://arc.liv.ac.uk/trac/SGE>`_

    Wallclock time
        The actual time taken to complete a job as measured by a clock on the
        wall or your wristwatch. 

    Snapshotted storage
        A storage area where the state of files/directories can be captured and saved at a moment in time.
        These snapshots are typically taken periodically to allow previous versions of files/directories to quickly be recovered.
        Some snapshotting systems only allow system administrators to access snapshots; 
        others, like that used on our HPC systems, permit users to directly view (read-only) snapshots.

        The system that provides snapshotting at TUOS stores snapshot data in the same filesystems as the 'live' data
        (on the same physical disks)
        so does not provide a true backup mechanism i.e. does not guard against disk/storage/filesystem failure.

        Also, users have no control over when snapshots are taken and snapshotting cannot log *why* files changed between snapshots:
        users should have their own mechanisms for meaningfully tracking changes to data, code and text files they care about, 
        with `git <https://rse.shef.ac.uk/blog/2020-03-29-git-github-remote/>`__ being the most obvious tool for tracking changes to code and text files.

    Mirrored backups
        Many TUOS storage areas use :term:`snapshotting <Snapshotted storage>` to allow users to recover older versions of files but this does not guard against disk/storage/filesystem failures.
        For this reason all data in certain storage areas is periodically copied (*mirrored*) to one or more separate storage systems in remote locations.
        These mirrored backups are only accessible to system administrators.
