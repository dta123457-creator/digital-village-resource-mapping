from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digital-village-resource-mapping",
    version="0.1.0",
    author="dta123457-creator",
    description="AI-powered GIS platform for Smart India Hackathon - Village resource mapping and infrastructure analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dta123457-creator/digital-village-resource-mapping",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.40.0",
        "folium>=0.14.0",
        "geopandas>=0.14.0",
        "pandas>=2.2.0",
        "numpy>=1.24.3",
        "flask>=3.0.0",
        "fastapi>=0.109.0",
        "sqlalchemy>=2.0.25",
    ],
)
