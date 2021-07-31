# brip - The Brython Package Installer

`brip` stands for [Brython](https://brython.info/)'s pip.
It brings the Python packages ecosystem and the pip-like workflow to Brython-powered projects.

You can use `brip` to install packages from the [PyPI](https://pypi.org) and other indexes, into your different Brython project.


## Problem Statement

* Historically, most **brython-oriented** Python packages are
  pre-compiled into - and distributed as - a javascript file.
  This works well for those self-contained Python packages,
  but when/if a Python package has its own dependencies,
  there was no obvious way to declare and manage those dependencies.
* In general, there was no Pythonic way to install a **generic Python** package
  and their dependencies, directly from PyPI into your Brython project.

`brip` is developed to bring the PyPI ecosystem and the familiar pip-like workflow
to Brython-powered projects.


## Quickstart: A complete sample project

There is a complete sample project, [Easter](https://github.com/rayluo/easter),
to demonstrate how to use `brip`.


## Installation

Just run `pip install brip`.

It is recommended that you install `brip` into one central virtual environment,
*rather than* installing `brip` inside each of your brython project's environment.
(In fact, your Brython project technically does not need its own virtual environment.)

Installation on Linux and macOS:

```
python3 -m venv ~/venv_central
source ~/venv_central/bin/activate
pip install brip
```

Installation on Windows:

```
py -m venv $HOME\venv_central
$HOME\venv_central\Scripts\activate.bat
pip install brip
```


## Manual: Command-line usage

This manual assumes you use Linux or macOS.
Windows users please adjust the path separator in each sample.

* Install a package from [PyPI](https://pypi.org) into your Brython project's
  web root directory (i.e. the directory containing your `index.html`):

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


* Install several packages from [PyPI](https://pypi.org) into your Brython project's
  web root directory (i.e. the directory containing your `index.html`):

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


## Limitations

`brip` aims to bring the entire Python Package Index (PyPI) ecosystem to Brython.
However, in reality there are some limitations outside of the control of `brip`.

* Brython-powered applications are running inside a browser.
  The browser is a capable virtual machine in its own right.
  However, many Python packages are not expected to be run inside a browser.
  For example, file system behaves differently in Brython: Writing is impossible,
  and reading is limited to the folders accessible with an Ajax request.

* Brython itself only supports pure Python packages.
  That excludes packages which are partially written in C, such as `numpy`.
  Consequently, only those packages written in pure Python
  *and its entire dependency chain* written in pure Python, would work in Brython.

* Sometimes, even pure Python package might not work in Brython, due to some subtle
  [differences between Brython and CPython](https://brython.info/static_doc/en/stdlib.html).

* Unfortunately, there is currently no straightforward way to know
  whether a Python package would work in Brython.
  You probably have to rely on trial-and-error.
  Just use `brip` to install a package, use it in Brython environment,
  and see if the browser console logs any error.

Feel free to report those packages into
[brip's issue list](https://github.com/rayluo/brip/issues).
`brip` might not be in position to solve it directly,
but the community might be able to help.


## Recipe for Brython-friendly package's maintainers

While we mentioned in the Problem Statement that `brip` was mainly developed to
allow Brython app developers to pull generic Python packages from PyPI, for example:

```
# Inside the brequirements.txt, it contains the following line
charts.css.py>=0.4,<1
```

there is nothing wrong for a self-contained, Brython-friendly package to
be distributed as a javascript file, for example:

```html
<!-- Inside the index.html, it contains the following line -->
<script src='https://github.com/rayluo/charts.css.py/releases/download/0.4.0/charts.css.py-brython.js'></script>
```

Here, the term "Brython-friendly" is defined as a generic, pure Python package
that can be released to PyPI, but it is also designed to be able to work in Brython.

So, how do you - a Brython-friendly package's maintainer - generate that javascript file?

Here is how I pack my package
[`charts.css.py`](https://github.com/rayluo/charts.css.py/releases/tag/0.4.0)
into a `charts.css.py-brython.js`:

```
cd charts.css.py
brip install .
# Now a site-packages.brython.js is generated in current directory,
# containing the PyPI-ready project in current directory.
# I just need to rename it to charts.css.py-brython.js and distribute it.
```

While doing so, you may see a warning message on your console:

```
  DEPRECATION: A future pip version will change local packages to be built in-place without first copying to a temporary directory. We recommend you use --use-feature=in-tree-build to test your packages with this new behavior before it becomes the default.
   pip 21.3 will remove support for this functionality. You can find discussion regarding this at https://github.com/pypa/pip/issues/7555.
```

You can just ignore that message. It has no negative impact to your javascript outcome.

That warning message is expected to be gone once pip 21.3 becomes available
and you upgrade to it (by running `python -m pip install --upgrade pip`).

