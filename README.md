# brip - The Brython Package Installer

`brip` stands for [Brython](https://brython.info/)'s pip.
It brings the Python packages ecosystem and the pip-like workflow to Brython-powered projects.

You can use `brip` to install packages from the [PyPI](https://pypi.org) and other indexes, into your different Brython project.


## Installation

`brip` can be installed by `pip` with the name `brython-brip`.

It is recommended that you install `brip` into one central virtual environment,
*rather than* installing `brip` inside each of your brython project's environment.
(In fact, your Brython project technically does not need its own virtual environment.)

Installation on Linux and macOS:

```
python3 -m venv ~/venv_central
source ~/venv_central/bin/activate
pip install brython-brip
```

Installation on Windows:

```
py -m venv $HOME\venv_central
$HOME\venv_central\Scripts\activate
pip install brython-brip
```


## Quickstart

This quickstart assumes you use Linux or macOS.
Windows users please adjust the path separator in each sample.

* Install a package from [PyPI](https://pypi.org) into your Brython project's web root directory:

  ```
  cd my_brython_project_one/website
  brip install SomePackage
  ```

  Now a new `site-packages.brython.js` is generated in current directory,
  containing SomePackage *and its dependencies*.
  Your Brython project's `index.html` would just need to add a line
  `<script src="site-packages.brython.js"></script>`,
  from now on you can use `import some_package` inside your Brython project!

  Package installed by `brip` is obtained directly from PyPI.
  You do *NOT* need to install the package by `pip` first.


* List what packages are installed for current Brython project
  (or more precisely speaking, list packages contained in `site-packages.brython.js`):

  ```
  cd my_brython_project_one/website
  brip list
  ```

  Note:
  Packages installed by `brip` are not visible to `pip list`, and vice versa.
  Because their installation target are completely different.


* Install several packages from [PyPI](https://pypi.org) into your Brython project's web root directory:

  ```
  cd my_brython_project_two/website
  brip install -r brequirements.txt
  ```

  The file "**b**requirements.txt" has
  [a format identical to `pip`'s "requirements.txt"](https://pip.pypa.io/en/stable/cli/pip_install/#requirements-file-format),
  and it can be named whatever name you want.
  We recommend using a name *different than* pip's conventional "requirements.txt",
  though, such as "**b**requirements.txt",
  to remind you that its content are meant to be installed by `brip`, not by `pip`.


* Uninstalling a package ... is not directly supported, but can be achieved by
  organizing your full dependency list in a "**b**requirements.txt" file,
  and then use this pattern:

  ```
  cd my_brython_project_two/website

  # Use your editor to remove one package name
  edit brequirements.txt

  # Each install will OVERWRITE existing site-packages.brython.js
  brip install -r brequirements.txt
  ```


## Differences to `pip`

In `pip` you can do incremental installation.
If you run `pip install foo` and then `pip install bar`,
you would end up with both `foo` and `bar` installed.

But, due to some technical reason, `brip` always do overwrite installation.
If you run `brip install foo` and then `brip install bar`,
you would end up with only `bar` available in your Brython project.

Therefore, we recommend you always use a "**b**requirements.txt"
to organize your project's full dependency.
That way, any adjustment to such a file would be flushed to your Brython project
by next `brip install -r brequirements.txt`.

`brip` also only implements a small subset of `pip`.
Please refer to the command-line help `brip -h` or `brip install -h` etc..


## Packages compatibilities

Although `brip` theoretically gives you access to all packages on PyPI,
Brython will only accept those packages not only themselves implemented in pure Python,
but also their entire dependencies must be implemented in pure Python.

Even so, some packages still won't work.
Feel free to report those packages into
[brip's issue list](https://github.com/rayluo/brip/issues).
`brip` might not be in position to solve it directly,
but the community might be able to help.

