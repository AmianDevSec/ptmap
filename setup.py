from setuptools import setup, find_packages

setup(
    name="ptmap",
    version="1.1.0",
    description="Asynchronous path traversal fuzzer",
    author="AmianDevSec",
    author_email="amiandevsec@gmail.com",
    license="GPL-3.0",

    packages=find_packages(),

    include_package_data=False,

    install_requires=[
        "aiohttp>=3.9.0",
        "rich>=13.0.0",
        "typer>=0.12.0",
        "pyfiglet>=1.0.0",
    ],

    entry_points={
        "console_scripts": [
            "ptmap=ptmap.ptmap:run",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
    ],

    python_requires=">=3.10",
)
