import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helloworld", # Package name
    version="0.0.1",
    author="Rishav",
    author_email="rishavranjan08@gmail.com",
    description="Hello World App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.azc.ext.hp.com/rishav-ranjan/hello-world-app",
    project_urls={
        "Bug Tracker": "https://github.azc.ext.hp.com/rishav-ranjan/hello-world-app/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'flask<2.1'
    ],
    extras_require={
        'test': [
            'pytest<6.3'
        ],
        'server': [
            'gunicorn<20.2'
        ]
    }
)