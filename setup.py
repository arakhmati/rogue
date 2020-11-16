from distutils.core import setup
from setuptools import find_packages

setup(
    name="rogue",
    version="0.0.0",
    description="Rogue video game written using Python functional programming.",
    packages=find_packages(),
    entry_points="""
     [console_scripts]
     rogue=rogue.cli.rogue:rogue
    """,
)
