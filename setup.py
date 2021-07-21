import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telegraph_api",
    version="1.0.2",
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
    setup_requires=[
        "aiohttp==3.7.4.post0",
        "async-timeout==3.0.1",
        "attrs==21.2.0",
        "beautifulsoup4==4.9.3",
        "bs4==0.0.1",
        "certifi==2021.5.30",
        "chardet==4.0.0",
        "charset-normalizer==2.0.2",
        "idna==3.2",
        "multidict==5.1.0",
        "pip==21.1.3",
        "pydantic==1.8.2",
        "setuptools==57.1.0",
        "soupsieve==2.2.1",
        "typing-extensions==3.10.0.0",
        "urllib3==1.26.6",
        "yarl==1.6.3",
    ]
)
