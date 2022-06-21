# -*- coding: utf-8 -*-
import codecs
import os
import subprocess
import sys
from shutil import rmtree

from setuptools import setup,find_packages, Command
from baato import config

here = os.path.abspath(os.path.dirname(__file__))

long_description = ""
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()



class BaseCommand(Command):
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _run(self, s, command):
        try:
            self.status(s + "\n" + " ".join(command))
            subprocess.check_call(command)
        except subprocess.CalledProcessError as error:
            sys.exit(error.returncode)



class ValidateCommand(BaseCommand):
    """Support setup.py validate."""

    description = "Run Python static code analyzer (flake8), formatter (black) and unit tests (pytest)."

    user_options = [("test-target=", "i", "tests/{test-target}")]

    def initialize_options(self):
        self.test_target = ""

    def run(self):
        self._run(
            "Installing test dependencies ...",
            [sys.executable, "-m", "pip", "install", "-r", f"{here}/requirements.txt"],
        )
        self._run("Running black ...", [sys.executable, "-m", "black", f"{here}/baato"])
        self._run(
            "Running flake8 for legacy packages ...", [sys.executable, "-m", "flake8", f"{here}/baato"]
        )

        self._run(
            "Running unit tests ...",
            [
                sys.executable,
                "-m",
                "pytest",
            ],
        )

class UploadCommand(BaseCommand):
    """Support setup.py upload."""

    description = "Build and publish the package."

    def run(self):
        self._run(
            "Installing upload dependencies ...",
            [sys.executable, "-m", "pip", "install", "wheel"],
        )
        try:
            self.status("Removing previous builds ...")
            rmtree(os.path.join(here, "dist"))
            rmtree(os.path.join(here, "build"))
        except OSError:
            pass

        self._run(
            "Building Source and Wheel (universal) distribution ...",
            [sys.executable, "setup.py", "sdist", "bdist_wheel", "--universal"],
        )
        self._run(
            "Installing Twine dependency ...",
            [sys.executable, "-m", "pip", "install", "twine"],
        )
        self._run(
            "Uploading the package to PyPI via Twine ...",
            [sys.executable, "-m", "twine", "upload", "--repository", "testpypi", "dist/*"],
        )

setup(
    name='baato',
    version=config.__version__,
    description='Baato API for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["Baato", "Python", "DRY"],
    author='Kathmandu Living Labs Consult',
    author_email='klltech@gmail.com',
    url='https://github.com/baato/baato-python',
    license='MIT License',
    packages=find_packages(
        exclude=[
            "docs",
            "tests",
            "tests.*",
            "tutorial",
        ]
    ),
    include_package_data=True,
    install_requires=[
        "requests",
        "decorator",
        "certifi",
    ],
    python_requires='>=3.6',
    setup_requires=['setuptools_scm'],
    cmdclass={
        "validate": ValidateCommand,
        "upload": UploadCommand,
    },
)
