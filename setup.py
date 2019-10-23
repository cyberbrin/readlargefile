import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readlargefile",
    version="1.0.4",
    author="xbn",
    author_email="xmgit@outlook.com",
    description="Large text file reader.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xmbin/readlargefile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    keywords='Large textfile reader',
    install_requires=[],
    python_requires='~=3.7'
)
