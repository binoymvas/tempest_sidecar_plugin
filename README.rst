Sidecar Tempest Plugin
=====================
Basic Tempest plugin structure that runs a sidecar test case.

============
Installation
============
When Tempest runs, it will automatically discover the installed plugins. So we just need to install the Python packages that contains the plugin.

Clone the repository in your machine and install the package from the src tree:

.. code-block:: bash

    $ cd tempest-sidecar-plugin
    $ sudo pip install -e .
    
============
How to run the tests
============
1. To validate that Tempest discovered the test in the plugin, you can run:

   .. code-block:: bash 

    $ tempest run --workspace cloud-01 --list-tests
    

   This command will show your complete list of test cases inside the plugin.


2. You can run the test cases by name or running the set names that they used as decorator  

   .. code-block:: bash  
    
    $  tempest run --workspace cloud-01  --regex tempest_sidecar_plugin.tests.api.test_sidecar.TestTempestSidecar
