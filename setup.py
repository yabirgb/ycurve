import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ycurve",
    version="1.0.0",
    author="Yabir Garcia",
    author_email="yabirg@protonmail.com",
    description="Library to work with elliptic curves on characteristic 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yabirgb/ycurve",
    project_urls={
        "Bug Tracker": "https://github.com/yabirgb/ycurveissues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "ycurve"},
    packages=setuptools.find_packages(where="ycurve"),
    python_requires=">=3.6",
)