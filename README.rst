All Package Index
=================

This repository contains scripts for parsing module files, generating documentation, and syncing with the HPC documentation repository.
These scripts automate the documentation process for an All Package Index section of our HPC Stanage cluster documentation.

The generated files for each package found on the given module paths includes:

* Description
* Sidebar - Latest version available on each architecture, date module file was last modified, and URL.
* Versions available - as module load commands in grouped tabs (for each architecture).
* Notes - detailing how to view build logs, etc.
* Dependencies - Shows the depenedenices for the latest version (across architectures), each is a link to it's respective page. 
 
Each of the above is imported into a package's page when built, this allows re-use of these imports 
elsewhere in the documentation.

TODO
----

- [ ] Support any number of architectures
 

Scripts
--------
.. code-block::

 ├── README
 ├── collect_data.py  parses module files in modulepaths for each arch
 ├── config.py        configuration file
 ├── config.yml       configuration for hpc-rocket
 ├── graph.py         creates markdown files for force directed graph in Obsidian
 ├── main.py          produces *.rst files, running collect_data.py if not already run today
 ├── run.sh
 ├── setup_local.sh   activates required environment, generating it if doesn't exist 
 ├── slurm.sh         job script run collect_data.py on hpc cluster
 └── sync_stacks.sh   syncs *rst files into hpc docs repo
 
Usage
-----
After modifying config.py and config.yml file for your system:

.. code-block:: bash 
 
 chmod +x run.sh setup_local.sh sync_stacks.sh
 ./sync_stacks.sh

config.py
---------
The configuration setup in config.py includes: 

Output directories which will later be synced with the documentation repo:

STACKS_DIR = "results/stanage/software/stubs/"
IMPORTS_DIR = "results/referenceinfo/imports/stanage/packages/"
CUSTOM_DIR = "results/referenceinfo/imports/stanage/packages/custom/"

Input parameters such as the modulepaths which we wish to parse, title(s) for the stack(s) and output directories for each stack: 

.. code-block:: python
 
 modulepaths = {
     'icelake': "/opt/apps/tuos/el9/modules/live/all:/opt/apps/tuos/common/modules/easybuild-only/all:/opt/apps/tuos/common/modules/live/all",
     'znver3': "/opt/apps/tuos/el9-znver3/modules/live/all:/opt/apps/tuos/common/modules/easybuild-only/all:/opt/apps/tuos/common/modules/live/all"
 }
 
 titles = [
     "Icelake and Znver (OS: Rocky 9) Package Versions"
 ]
 
 output_dirs = [
     "el9-icelake-znver-stanage"
 ]

In this example, the directory which the category directories and package files will be stored:

``/stanage/software/stubs/el9-icelake-znver-stanage/{All,Bio,etc}``

The title of the stack is 'Icelake and Znver (OS: Rocky 9) Package Versions'.

The module files which are located in modulepaths are parsed, in this case one set for each architecture.

Functions
^^^^^^^^^
Below are some of the main.py functions, which we may wish to customise:

.. code-block:: python

 process_modulepath(modulepaths, title, output_dir)
 # Processes data parsed from modulepaths which is then passed to the following functions: 
 
 write_package_file(category_dir, category, package, output_dir)
 write_sidebar_file(package, category, latest_version_info, output_dir)
 write_description_file(package, latest_info, output_dir)
 write_installation_file(package, latest_info, output_dir)
 write_custom_file(package, output_dir)
 write_dependencies(dependencies, output_dir, category, package, package_ref)
 write_ml_file(package, package_infos, output_dir)

Below are some of the main collect_data.py functions:

.. code-block:: python

 collect_data():
 process_broken_symlinks():
 extract_lua_info(lua_file_path):
 extract_installer(file_path):
