:orphan:

.. include:: /referenceinfo/imports/decommissioned/sharc_decom.rst

.. include:: /referenceinfo/imports/decommissioned/decom_watermark.rst

.. _jh_quickstart: 

JupyterHub on ShARC: Quickstart
===============================

A brief walk-through for the eager.

#. Open a web browser and browse to: ::

       https://jupyter-sharc.shef.ac.uk

#. Log in when prompted using your University username and password.

#. Click **Start My Server**.

#. Under **Spawner options** you specify the resources you require for your Jupyter session on ShARC.  Here, try:

    * *Project*: *default*
    * *Job queue*: *any*
    * *Email address*: your email address
    * *CPU cores*: 1
    * *Parallel Environment*: None
    * *RAM per CPU core* (in GB): 4 
    * *GPUs per CPU core*: 0
    * *Notebook session runtime*: can't be changed

#. Click **Spawn** and wait for your session to start.  If the cluster is very busy then there may not be sufficient resources for this, so the session *spawning* may time-out. 

#. Once your Jupyter session has spawned you should see a list of the files in your home directory on ShARC.  Click **New** then **Python [conda env:anaconda3-4.2.0]**.

#. You should now see an empty Notebook.  

**TODO**: finish

