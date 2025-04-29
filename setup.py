from setuptools import setup, find_packages
setup(
    name="termc",
    version="v0.9.2",
    author="LBY_L",
    license="GNU General Public License 3.0 (GPL 3.0)",
    description="A simple script to download and execute Minecraft servers",
    packages=find_packages(),
    install_requires=[
        "yaspin",
        "InquirerPy",
        "psutil"
    ],
    keywords=["cli", "tui"],
    entry_points={"console_scripts": "termc = termc.termc:Init"},
    python_requires=">=3.10",
)
