"""
This is not finalized. Not sure whether this folder should be installable.
"""

from setuptools import setup
import re

with open("src/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="SamsungDataAnalysis",
    version=version
    #install_requires=[]
)
