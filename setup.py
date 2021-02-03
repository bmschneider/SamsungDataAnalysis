"""
This is not finalized. Not sure whether this folder should be installable.
"""

from setuptools import setup, find_packages
import re

with open("src/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="sda",
    version=version,
    packages=find_packages(include=['src', 'src.*'])
    #install_requires=[]
)
