import setuptools
from version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkhtmlview",
    version=VERSION,
    author="Palash Bauri",
    keywords='tkinter html developement webview',
    description="View Simple HTML docs on tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bauripalash/tkhtmlview",

    project_urls={
        'Documentation': 'https://github.com/bauripalash/tkhtmlview',
        'Funding': 'https://github.com/bauripalash',
        'Source': 'https://github.com/bauripalash/tkhtmlview',
        'Tracker': 'https://github.com/bauripalash/tkhtmlview/issues',
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',


        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.4.*",
    install_requires=['Pillow>=5.3.0','requests>=2.22.0'],
)
