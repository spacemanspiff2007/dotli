from pathlib import Path

import setuptools
import typing

# Load version number
SETUP_PY = Path(__file__)

version: typing.Dict[str, str] = {}
with (SETUP_PY.with_name('src') / 'dotli' / '__version__.py').open() as fp:
    exec(fp.read(), version)
assert version
assert version['__version__']
__version__ = version['__version__']
print(f'Dotli Version: {__version__}')
print('')

# don't load file for tox-builds
readme = SETUP_PY.with_name('readme.md')
long_description = ''
if readme.is_file():
    with readme.open("r", encoding='utf-8') as fh:
        long_description = fh.read()

setuptools.setup(
    name="dotli",
    version=__version__,
    author="spaceman_spiff",
    # author_email="",
    description="An easy way to flatten and unflatten dicts and lists",
    keywords=[
        'json',
        'flatten',
        'unflatten',
        'unpack',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spacemanspiff2007/dotli",
    project_urls={
        'GitHub': 'https://github.com/spacemanspiff2007/dotli',
    },
    packages=setuptools.find_packages('src', exclude=['tests*']),
    package_dir={'': 'src'},
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ]
)
