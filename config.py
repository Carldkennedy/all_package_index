import datetime

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

broken_symlinks_file = f"broken-symlinks.log"
log_file_path = f"log-collect-data.log"
main_log_file= f"main-update-packages.log"

DATA_FILE = "collected-data.pkl"
STACKS_DIR = "stanage/software/stubs/"
IMPORTS_DIR = "referenceinfo/imports/stanage/packages/"
CUSTOM_DIR = "referenceinfo/imports/stanage/packages/custom/"

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

# Define the path for the SLURM interactive session include file
SLURM_INTERACTIVE_SESSION_IMPORT = "referenceinfo/imports/scheduler/SLURM/common_commands/srun_start_interactive_session_import_stanage.rst"

module_classes = {
    "base": "Default module class",
    "ai": "Artificial Intelligence (incl. Machine Learning)",
    "astro": "Astronomy, Astrophysics and Cosmology",
    "bio": "Bioinformatics, biology and biomedical",
    "cae": "Computer Aided Engineering (incl. CFD)",
    "chem": "Chemistry, Computational Chemistry and Quantum Chemistry",
    "compiler": "Compilers",
    "data": "Data management & processing tools",
    "debugger": "Debuggers",
    "devel": "Development tools",
    "geo": "Earth Sciences",
    "ide": "Integrated Development Environments (e.g. editors)",
    "lang": "Languages and programming aids",
    "lib": "General purpose libraries",
    "math": "High-level mathematical software",
    "mpi": "MPI stacks",
    "numlib": "Numerical Libraries",
    "perf": "Performance tools",
    "quantum": "Quantum Computing",
    "phys": "Physics and physical systems simulations",
    "system": "System utilities (e.g. highly depending on system OS and hardware)",
    "toolchain": "EasyBuild toolchains",
    "tools": "General purpose tools",
    "vis": "Visualisation, plotting, documentation and typesetting"
}
