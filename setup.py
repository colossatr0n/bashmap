import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bashmap",
    version="0.1.0",
    author="colossatr0n",
    author_email="29556317+colossatr0n@users.noreply.github.com",
    description="BashMap converts shell commands into an argument dictionaries.",
    entry_points = {
        'console_scripts': ['bashmap=bashmap.bashmap:main']
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colossatr0n/bashmap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)