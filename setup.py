from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="CharacTER",
    version="0.0.1",
    description="Translation Edit Rate on character level",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords="machine-translation machine-translation-evaluation evaluation mt",
    package_dir={"": "src"},
    packages=find_packages("src"),
    url="https://github.com/BramVanroy/CharacTER",
    author="Bram Vanroy",
    author_email="bramvanroy@hotmail.com",
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    project_urls={
        "Issue tracker": "https://github.com/BramVanroy/CharacTER/issues",
        "Source": "https://github.com/BramVanroy/CharacTER"
    },
    python_requires=">=3.7",
    install_requires=["Levenshtein"]
)
