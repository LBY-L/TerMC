import json
from setuptools import setup, find_packages

# Función para obtener la versión desde el archivo JSON
with open('termc/MANIFIEST.json', 'r') as file:
    VERSION = json.load(file)["TerMCVersion"]

# Configuración de setuptools
setup(
    name="termc",
    version=VERSION,  # Usamos la función para obtener la versión
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
    package_data={"termc": ["MANIFIEST.json"]},  # Aseguramos que el archivo JSON se incluya en el paquete
    python_requires=">=3.10",
)
