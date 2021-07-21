import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telegraph_api",
    version="1.0.0",
    author="ivanprogramming",
    description="Asynchronus Python wrapper for telgra.ph API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IvanProgramming/telegraph_api",
    project_urls={
        "Bug Tracker": "https://github.com/IvanProgramming/telegraph_api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "telegraph_api"},
    packages=setuptools.find_packages(where="telegraph_api"),
    python_requires=">=3.8",
)