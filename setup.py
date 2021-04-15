from setuptools import find_packages, setup

def readme():
    with open("README.md", "r") as f:
        return f.read()

def requirements():
    with open("requirements.txt") as f:
        req = [line.rstrip("\n") for line in f]
        return req

setup(
    name="dancebots",
    version="1.0.0",
    description="A Python package for programming Dancebots",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/r-oung/dancebots-python",
    author="Raymond Oung",
    author_email="raymond.oung@alumni.ethz.ch",
    license="MIT",
    keywords="robot education STEM",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements(),
    python_requires=">=3.6",
)
