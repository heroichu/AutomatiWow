from setuptools import setup, find_packages

setup(
    name="wow-auto-key",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="魔兽世界自动按键脚本",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/wow-auto-key",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pywin32>=227",
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
    entry_points={
        "console_scripts": [
            "wow-auto-key=main:main",
        ],
    },
)