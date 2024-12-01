from setuptools import setup, find_packages

setup(
    name="codebase",
    version="1.0.0",
    author="DJ",
    author_email="dibyajyotid2024@gmail.com",
    description="A simple example package",
    long_description=open('README.md').read(),  # You can load a long description from a file like README.md
    long_description_content_type="text/markdown",
    url="https://github.com/username/my_package",
    packages=find_packages(),
    install_requires=[
        "rich",
        "pyfiglet",
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'codebase=__main__',  # Entry point for a CLI tool
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
