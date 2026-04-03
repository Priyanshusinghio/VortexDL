from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="vortexdl",
    version="1.0.0",
    author="VortexDL Contributors",
    description="A powerful, extensible video & audio downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/you/vortexdl",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "yt-dlp>=2024.1.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "PyYAML>=6.0",
        "aiohttp>=3.9.0",
        "aiohttp-cors>=0.7.0",
        "mutagen>=1.47.0",
        "Pillow>=10.0.0",
        "humanize>=4.0.0",
        "packaging>=23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
            "responses>=0.24.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "vortexdl=vortexdl.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet",
    ],
    include_package_data=True,
    package_data={
        "vortexdl": ["web/templates/*.html", "web/static/**/*"],
    },
)
