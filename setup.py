import setuptools
from distutils.command.install_data import install_data

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chase",
    version="1.0",
    author=u"Piotr Ruciński",
    description="A simulation based on a wolf chasing sheep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['chase.__main__', 'chase.simulation'],
    data_files=[('config', ['config/config.ini'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
