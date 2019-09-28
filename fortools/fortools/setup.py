import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortools",
    version="0.0.1",
    author="5ha0",
    author_email="bobbaeha@gmail.com",
    description="forensics python library fortools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5ha0/fortools/fortools",
    packages=setuptools.find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
    ],
)