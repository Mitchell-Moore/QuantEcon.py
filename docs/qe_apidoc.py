"""
Our version of sphinx-apidoc

@author : Spencer Lyon
@date : 2014-07-16

This file should be called from the command line. It accepts one
additional command line parameter. If we pass the parameter `single`
when running the file, this file will create a single directory named
modules where each module in quantecon will be documented. The index.rst
file will then contain a single list of all modules.

If no argument is passed or if the argument is anything other than
`single`, two directories will be created: models and tools. The models
directory will contain documentation instructions for the different
models in quantecon, whereas the tools directory will contain docs for
the tools in the package. The generated index.rst will then contain
two toctrees, one for models and one for tools.

Examples
--------
$ python qe_apidoc.py  # generates the two separate directories
$ python qe_apidoc.py  foo_bar  # generates the two separate directories
$ python qe_apidoc.py single  # generates the single directory


Notes
-----
This file can also be run from within ipython using the %%run magic.
To do this, use one of the commands above and replace `python` with
`%%run`

"""
import os
import sys
from glob import glob


######################
## String Templates ##
######################
module_template = """{mod_name}
{equals}

.. automodule:: quantecon.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

markov_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.markov.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

model_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.models.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

solow_model_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.models.solow.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

random_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.random.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

util_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.util.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

all_index_template = """=======================
QuantEcon documentation
=======================

Auto-generated documentation by module:

.. toctree::
   :maxdepth: 2

   {generated}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

split_index_template = """=======================
QuantEcon documentation
=======================

The `quantecon` python library is composed of two main section: models
and tools. The models section contains implementations of standard
models, many of which are discussed in lectures on the website `quant-
econ.net <http://quant-econ.net>`_.

.. toctree::
   :maxdepth: 2

   markov
   models
   random
   tools

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

split_file_template = """{name}
{equals}

.. toctree::
   :maxdepth: 2

   {files}
"""

######################
## Helper functions ##
######################


def source_join(f_name):
    return os.path.join("source", f_name)

####################
## Main functions ##
####################


def all_auto():
    # Get list of module names
    mod_names = glob("../quantecon/[a-z0-9]*.py")
    mod_names = map(lambda x: x.split('/')[-1], mod_names)

    # Ensure source/modules directory exists
    if not os.path.exists(source_join("modules")):
        os.makedirs(source_join("modules"))

    # Write file for each module
    for mod in mod_names:
        name = mod.split(".")[0]  # drop .py ending
        new_path = os.path.join("source", "modules", name + ".rst")
        with open(new_path, "w") as f:
            gen_module(name, f)

    # write index.rst file to include these autogenerated files
    with open(source_join("index.rst"), "w") as index:
        generated = "\n   ".join(map(lambda x: "modules/" + x.split(".")[0],
                                     mod_names))
        temp = all_index_template.format(generated=generated)
        index.write(temp)


def model_tool():
    # list file names with markov
    markov_files = glob("../quantecon/markov/[a-z0-9]*.py")
    markov = map(lambda x: x.split('/')[-1][:-3], markov_files)
    # Alphabetize
    markov.sort()

    # list file names with models
    mod_files = glob("../quantecon/models/[a-z0-9]*.py")
    models = map(lambda x: x.split('/')[-1][:-3], mod_files)
    # Alphabetize
    models.sort()

    # list file names with models.solow
    solow_files = glob("../quantecon/models/solow/[a-z0-9]*.py")
    solow = map(lambda x: x.split('/')[-1][:-3], solow_files)
    # Alphabetize
    solow.sort()

    # list file names with random
    random_files = glob("../quantecon/random/[a-z0-9]*.py")
    random = map(lambda x: x.split('/')[-1][:-3], random_files)
    # Alphabetize
    random.sort()

    # list file names of tools (base level modules)
    tool_files = glob("../quantecon/[a-z0-9]*.py")
    tools = map(lambda x: x.split('/')[-1][:-3], tool_files)
    # Alphabetize
    tools.sort()
    
    # list file names of utilities
    util_files = glob("../quantecon/util/[a-z0-9]*.py")
    util = map(lambda x: x.split('/')[-1][:-3], util_files)
    # Alphabetize
    util.sort()

    for folder in ["markov","models","models/solow","random","tools","util"]:
        if not os.path.exists(source_join(folder)):
            os.makedirs(source_join(folder))

    # Write file for each markov file
    for mod in markov:
        new_path = os.path.join("source", "markov", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(markov_module_template.format(mod_name=mod, equals=equals))

    # Write file for each model
    for mod in models:
        new_path = os.path.join("source", "models", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(model_module_template.format(mod_name=mod, equals=equals))

    # Write file for each model.solow
    for mod in solow:
        new_path = os.path.join("source", "models", "solow", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(solow_model_module_template.format(mod_name=mod, equals=equals))  

    # Write file for each random file
    for mod in random:
        new_path = os.path.join("source", "random", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(random_module_template.format(mod_name=mod, equals=equals))

    # Write file for each tool (base level modules)
    for mod in tools:
        new_path = os.path.join("source", "tools", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(module_template.format(mod_name=mod, equals=equals))

    # Write file for each utility
    for mod in util:
        new_path = os.path.join("source", "util", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(util_module_template.format(mod_name=mod, equals=equals))

    # write (index|models|tools).rst file to include autogenerated files
    with open(source_join("index.rst"), "w") as index:
        index.write(split_index_template)

    mark = "markov/" + "\n   markov/".join(markov)
    mods = "models/" + "\n   models/".join(models)
    mods = mods  + "\n   solow/"                                 #Add solow sub directory to models
    rand = "random/" + "\n   random/".join(random)
    tlz = "tools/" + "\n   tools/".join(tools)
    utls = "util/" + "\n   util/".join(util)
    toc_tree_list = {"markov":mark,
                     "models": mods,
                     "tools": tlz,
                     "random":rand,
                     "util":utls,
                     }

    for f_name in ("markov","models","random","tools","util"):
        with open(source_join(f_name + ".rst"), "w") as f:
            temp = split_file_template.format(name=f_name.capitalize(),
                                              equals="="*len(f_name),
                                              files=toc_tree_list[f_name])
            f.write(temp)

if __name__ == '__main__':
    if "single" in sys.argv[1:]:
        all_auto()
    else:
        model_tool()
