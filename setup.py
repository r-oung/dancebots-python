import setuptools


def readme():
    with open("README.md", "r") as f:
        return f.read()

def requirements():
    with open("requirements.txt") as f:
        req = [line.rstrip('\n') for line in f]
        print(req)

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
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, macOS, Windows",
    ],
    python_requires=">=3.6",
)