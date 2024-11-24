from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docker-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A GUI application for Docker management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docker-manager",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pillow",
        "cairosvg",
    ],
    package_data={
        "docker_manager": ["resources/*"],
    },
    entry_points={
        "console_scripts": [
            "docker-manager=docker_manager.docker_manager:main",
        ],
    },
)