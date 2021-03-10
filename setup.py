import setuptools


def readme():
    with open("README.md", "r") as f:
        return f.read()


setuptools.setup(
    name="dancebots",
    version="1.0.0",
    description="Python package for DanceBots",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="R. Oung",
    author_email="raymond.oung@alumni.ethz.ch",
    url="https://github.com/r-oung/dancebots-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "Pillow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu, macOS",
    ],
    python_requires=">=3.6",
)