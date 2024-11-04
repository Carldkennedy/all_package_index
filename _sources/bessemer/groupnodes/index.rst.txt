.. _groupnodes_bessemer:

Department or research group-specific nodes in Bessemer
=======================================================

.. toctree::
    :maxdepth: 1
    :glob:

    ./dcs-gpu-nodes
    ./dcs-acad-gpu-nodes

.. _slurm_access_priv_nodes:

Running Slurm batch jobs or interactive sessions on private nodes
-----------------------------------------------------------------

To run Slurm jobs on private nodes you will need to specify at least one of:

* A Slurm Account
* A Slurm Partition
* A Slurm QoS (Quality of Service)

You will be told what to specify when you are granted access to the private nodes.

To start an interactive session on a private node you want something like the following: ::

   srun --account=SOMEACCOUNT --partition=SOMEPARTITION --qos=SOMEQOS --pty /bin/bash -i

To submit a batch start that will run on private node(s)
you want something like the following in your batch job submission script: ::

   #!/bin/bash
   #SBATCH --account=SOMEACCOUNT
   #SBATCH --partition=SOMEPARTITION
   #SBATCH --qos=SOMEQOS
