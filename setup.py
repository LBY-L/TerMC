from setuptools import setup, find_packages
# Setting up
setup(
    name="termc",
    python_requires='>=3.10',
    version="0.8",
    author="LBY_L",
    license='GNU General Public License 3.0 (GPL 3.0)',
    description="TerMC a cli dash to install and run minecraft servers 🎇",
    entry_points={
        'console_scripts': 'termc = termc.__init__:__main__'
    },
    packages=find_packages(),
    install_requires=['yaspin', 'InquirerPy'],
    keywords=['cli', 'tui']
)
# Why i keeping doing this things...
