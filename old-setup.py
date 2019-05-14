from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='autoBWF',
    version='3.2.3',
    author="Michael Andrec/Ukrainian History and Education Center",
    author_email="m.andrec@UkrHEC.org",
    description="Alternative opinionated GUI for FADGI BWFMetaEdit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ukrainian-History/autoBWF",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'appdirs',
        'PyQt5',
    ],
    entry_points={
        'console_scripts': ['autoBWF=autoBWF:main',
                            'autolame=autolame:main'],
    }
)
