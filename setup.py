import setuptools
import tkhtmlview

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkhtmlview",
    version=tkhtmlview.VERSION,
    author="Palash Bauri",
    author_email="hey@palashbauri.in",
    description="View Simple HTML docs on tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bauripalash/tkhtmlview",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4.*",
    install_requires=['Pillow>=5.3.0','requests>=2.22.0'],
)
