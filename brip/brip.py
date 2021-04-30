import argparse
import sys
import tempfile
import subprocess
import os
import shutil
import json


__version__ = "0.1.0"

_site_packages = "site-packages"
_site_packages_filename = "{}.brython.js".format(_site_packages)


def main():
    caveat = ('Unlike "pip install ..."\'s incremental behavior, '
        'each run of "brip install ..." will overwrite the existing {site}.'
        ).format(site=_site_packages_filename)
    parser = argparse.ArgumentParser(
        description="A pip-like tool to install python packages into Brython app",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-V", "--version", action='version',
        version='%(prog)s {ver} from {file} (python {py_major}.{py_minor})'.format(  # Mimic pip
            ver=__version__, file=os.path.abspath(__file__),
            py_major=sys.version_info[0], py_minor=sys.version_info[1]),
        help="Show version and exit")
    subparsers = parser.add_subparsers(
        title="Commands",  # It replaces the default "Positional arguments" text
        #required=True,  # Python 3.7+, but it needs an explicit `dest`. See below.
        dest="command",  # Workaround for https://bugs.python.org/issue29298
        )

    parser_install = subparsers.add_parser(
        'install',
        help="""Install packages into {site}. CAVEAT: {caveat}
            """.format(site=_site_packages_filename, caveat=caveat),
        usage="""
            brip install <requirement specifier> ...
            brip install -r <requirements file>

            CAVEAT: {}""".format(caveat),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_install.add_argument(
        "packages", nargs="*", metavar="<requirement specifier>",
        help="CAVEAT: {}".format(caveat))
    parser_install.add_argument(
        "-r", "--requirement", metavar="<file>",
        help="Install from the given requirements file.")
    parser_install.add_argument(
        "-t", "--target", metavar="<dir>", default=".",
        help="Install packages into <dir>/{}.".format(_site_packages_filename))
    parser_install.set_defaults(func=_install, parser=parser_install)

    parser_list = subparsers.add_parser(
        'list',
        help="List installed packages from {}".format(_site_packages_filename),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_list.add_argument(  # Implements https://github.com/pypa/pip/issues/5686
        "-t", "--target", metavar="<dir>", default=".",
        help="List packages from <dir>/{}".format(_site_packages_filename))
    parser_list.set_defaults(func=_list, parser=parser_list)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit("Need a command to run")
    args.func(args)


def _install(args):  # Depends on Python 3.5+ for system.run()
    if (args.packages and args.requirement) or (
            (not args.packages) and (not args.requirement)):
        args.parser.print_help()
        sys.exit("Need a package name or a requirements file")
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            sources = args.packages if args.packages else ["-r", args.requirement]
            # `brython-cli --add_package foo` would NOT include foo's dependency.
            # We use pip. As a by-product, it does not pollute the current environment.
            subprocess.run(["pip", "install"] + sources + ["-t", tempdir], check=True)

            # We could use `brython-cli --modules` to scan everything (*.py, including *.html)
            # and build one brython_modules.js, which will typically be 2.4MB only,
            # (slimmer than the standard brython_stdlib.js which is 3.8MB).
            # But that approach has its own challenges:
            # * There needs to be a LOCAL brython_stdlib.js to bootstrap.
            #   But that is unavailable if the current project chose to load it from CDN.
            # * Its build process would become mandatory even when no 3rd-party package is used
            #
            # So, we choose `brython-cli --make_package` to convert Lib/site-packages/*
            # into one site-packages.brython.js,
            # and then load it after brython.js and brython_stdlib.js.
            # Besides, it feels logically right to have brython and its stdlib hosted from CDN,
            # and the site-packages hosted on this website.
            cwd = os.getcwd()
            os.chdir(tempdir)
            subprocess.run(["brython-cli", "--make_package", _site_packages], check=True)
            os.chdir(cwd)
            shutil.copy(os.path.join(tempdir, _site_packages_filename), args.target)
    except subprocess.CalledProcessError:
        print("Installation aborted")  # Presumably, the called command already printed their errors


def _list(args):
    filename = os.path.join(args.target, _site_packages_filename)
    if not os.path.exists(filename):
        return
    with open(filename) as f:
        lines = f.readlines()
    # Based on the _site_packages_filename format. Subject to change.
    packages = json.loads(lines[1].split("=", maxsplit=1)[1])
    print("\n".join(sorted({
        name.split(".")[0]  # Converge "package.module" into "package"
        for name in packages.keys() if name != "$timestamp"})))


if __name__ == "__main__":
    main()

