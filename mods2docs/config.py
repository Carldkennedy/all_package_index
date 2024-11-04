import datetime
from pathlib import Path

# Outputs
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

DATA_FOLDER = Path("data")

broken_symlinks_file = DATA_FOLDER / "broken-symlinks.log"
log_file_path = DATA_FOLDER / "log-collect-data.log"
main_log_file = DATA_FOLDER / "main-update-packages.log"

DATA_FILE = DATA_FOLDER / "collected-data.pkl"
stacks_dir = "stanage/software/stubs/"
imports_dir = "referenceinfo/imports/stanage/packages/"
custom_dir = "referenceinfo/imports/stanage/packages/custom/"
STACKS_DIR = DATA_FOLDER / stacks_dir 
IMPORTS_DIR = DATA_FOLDER / imports_dir
CUSTOM_DIR = DATA_FOLDER / custom_dir

# Inputs
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
