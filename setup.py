from setuptools import setup, find_packages

# Setting up
setup(
    name="termc",
    python_requires=">=3.10",
    version="0.8.3",
    author="LBY_L",
    license="GNU General Public License 3.0 (GPL 3.0)",
    description="A simple script to download and execute Minecraft servers",
    entry_points={"console_scripts": "termc = termc.__init__:__main__"},
    packages=find_packages(),
    install_requires=["yaspin", "InquirerPy", "psutil"],
    keywords=["cli", "tui"],
)
# Why i keeping doing this things...
