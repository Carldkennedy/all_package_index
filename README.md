All Package Index
=================

This repository contains scripts for parsing module files, generating documentation, and syncing with the HPC documentation repository.
These scripts automate the documentation process for an "All Package Index" section of the HPC Stanage cluster documentation, including
configuration and handling dependencies for various architectures.

The generated files for each package found on the given module paths includes:

* Description
* Sidebar - Latest version available on each architecture, date module file was last modified, and URL.
* Versions available - as module load commands in grouped tabs (for each architecture).
* Notes - detailing how to view build logs, etc.
* Dependencies - Shows the dependencies for the latest version (across architectures), each is a link to it's respective page.
 
Each of the above is imported into a package's page when built, this allows re-use of these imports 
elsewhere in the documentation.

## TODO

- [ ] Support any number of architectures
 
## Setup and Usage

### Configuration

To configure the necessary parameters, use config.py and config.yml:

config.py defines output directories for generated documentation and other key paths.
config.yml includes HPC-Rocket configuration for starting a batch job on cluster.

``config.py`` defines output directories for generated documentation and other key paths. 

Output directories: Directories synced with the documentation repo:

```python

    STACKS_DIR = "results/stanage/software/stubs/"
    IMPORTS_DIR = "results/referenceinfo/imports/stanage/packages/"
    CUSTOM_DIR = "results/referenceinfo/imports/stanage/packages/custom/"
```

Module Paths and Titles: Paths for module files to parse, titles for stacks, and output directories:

```python
 
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
```

In this example, the directory which the category directories and package files will be stored:

``/stanage/software/stubs/el9-icelake-znver-stanage/{All,Bio,etc}``

The title of the stack is 'Icelake and Znver (OS: Rocky 9) Package Versions'.

The module files which are located in modulepaths are parsed, in this case one set for each architecture.

### Scripts Overview

The repository includes several scripts and modules organised under mods2docs, each with a specific role in the pipeline:


    |____ README
    |____ run-hpc-rocket.sh    initiates slurm job on cluster
    |____ setup_local.sh       activates required environment, generating it if doesn't exist
    |____ slurm.sh             job script run collect_data.py on hpc cluster
    |____ sync_stacks.sh       syncs *rst files into hpc docs repo
    |____ mods2docs
    | |____ config.py          configuration file
    | |____ config.yml         configuration for hpc-rocket
    | |____ collect_data.py    parses module files in modulepaths for each arch
    | |____ utils.py           commonly used functions
    | |____ start_pipeline.py  produces *.rst files, running collect_data.py if not already run today
    | |____ writer
    | | |____ common.py        commonly used writer functions
    | | |____ obsidian.py      creates markdown files for force directed graph in Obsidian
    | | |____ rest.py          produces *.rst files for sphinx documentation
    | |____ parser
    | | |____ common.py
    | | |____ lmod.py          parses lua module files on modulepath


### Setting Up and Running Scripts

```bash 
   #Make scripts executable
   chmod +x run-hpc-rocket.sh setup_local.sh sync_stacks.sh
   # Set up local environment
   ./setup_local.sh
   # This script completes pipeline and pushes changes from a new branch to the remote repository
   ./sync_stacks.sh
```

## Pipeline Overview

The primary script, start_pipeline.py, orchestrates the data parsing and documentation generation pipeline:
.
.
.
.
.
.
.


### Writer modules

Below are some of the mods2docs functions, which we may wish to customise:

```python

 process_modulepath(modulepaths, title, output_dir)
 # Processes data parsed from modulepaths which is then passed to the following functions: 
 
 write_package_file(category_dir, category, package, output_dir)
 write_sidebar_file(package, category, latest_version_info, output_dir)
 write_description_file(package, latest_info, output_dir)
 write_installation_file(package, latest_info, output_dir)
 write_custom_file(package, output_dir)
 write_dependencies(dependencies, output_dir, category, package, package_ref)
 write_ml_file(package, package_infos, output_dir)
```

### Parser Modules

## Contributing

We welcome contributions to the All Package Index project! Whether you’d like to report a bug, suggest new features,
or improve the documentation, your help is invaluable to the project’s success. 
Please follow the guidelines below to ensure a smooth collaboration process.

.
.
.
.
.
.
