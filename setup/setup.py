"""
Singularity Delta Setup Configuration
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="SINGULARITY_DELTA",
    version="1.0.0",
    author="VISHAL THAKUR",
    author_email="vt83291@gmail.com",
    description="Deterministic Policy Verification Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyc3o/SINGULARITY_DELTA",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No dependencies!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "pylint>=2.15.0",
            "mypy>=0.991",
        ]
    },
    entry_points={
        "console_scripts": [
            "singularity-delta=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["schema/*.json", "examples/*.json"],
    },
)
