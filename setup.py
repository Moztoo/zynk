from setuptools import setup, find_packages

setup(
    name="zynk",
    version="0.1",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "rich",
        "feedparser",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "zynk = zynk.__main__:main"
        ]
    },
    author="R. Mostalac",
    description="Terminal News Feed Viewer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
)