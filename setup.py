import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grizzly-sql",
    version="0.1.4",
    author="Databases & Information Systems Group, TU Ilmenau",
    author_email="stefan.hagedorn@tu-ilmenau.de",
    description="A Python-to-SQL transpiler to work with relational databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbis-ilm/grizzly",
    license = "MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
