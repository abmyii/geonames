import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix
"""


setuptools.setup(
    name="geonames-lib",
    version="0.2",
    author="abmyii",
    author_email="abdurrahmaaniqbal@hotmail.com",
    description="Library for working with GeoNames dump",
    long_description=long_description,
    url="https://github.com/abmyii/geonames",
    packages=setuptools.find_packages(),
    py_modules=['geonames'],
    install_requires=['fuzzywuzzy', 'pandas'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
)
