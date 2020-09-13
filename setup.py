import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="spike2py",
    version="0.1.0",
    description="Import, parse and process data collected with Spike2",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinHeroux/spike2py",
    author="Martin Héroux",
    author_email="heroux.martin@gmail.com",
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["spike2py"],
    include_package_data=False,
    install_requires=["numpy>=1.19.1", "scipy>=1.5.2", "matplotlib>=3.3.1"],
    tests_require=["pytest>=6.0.1", "pytest-cov>=2.10.1", "pytest-mpl>= 0.11"]
)