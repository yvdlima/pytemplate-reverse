import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pytemplate_reverse",
    version="0.0.2",
    author="Yuri Vinicius Didone de Lima",
    author_email="yuri.vdl@gmail.com",
    description="Reverse-engineer the values of a string based on a template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yvdlima/pytemplate-reverse",
    packages=setuptools.find_packages(),
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
