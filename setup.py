from setuptools import setup, find_packages

setup(
    name="codebase", 
    version="1.0.0",  
    packages=find_packages(), 
    entry_points={
        "console_scripts": [
            "codebase=codebase.scripts:main",  # Replace with your entry point
        ],
    },
    install_requires=[
        "rich","pyvim","pyfiglet"
    ],
    python_requires=">=3.6",  # Minimum Python version
)
