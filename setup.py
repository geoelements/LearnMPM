"""A setuptools based setup module."""

from setuptools import setup, find_packages

def parse_meta(path_to_meta):
    with open(path_to_meta) as f:
        meta = {}
        for line in f.readlines():
            if line.startswith("__version__"):
                meta["__version__"] = line.split('"')[1]
    return meta

meta = parse_meta("LearnMPM/meta.py")

with open('README.md', encoding="utf8") as f:
    long_description = f.read()

setup(
    name='LearnMPM',
    version=meta['__version__'],
    description='Package for Surface Wave Processing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/geoelements/LearnMPM',
    author='Krishna Kumar',
    author_email='krishnak@utexas.edu',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',

        "License :: OSI Approved :: MIT License",

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='mpm learn 1d',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=["numpy", "matplotlib"],
    extras_require={
        'dev': ['coverage', 'tox', 'sphinx', 'sphinx_rtd_theme'],
    },
    package_data={
    },
    data_files=[
    ],
    entry_points={
    },
    project_urls={
        'Bug Reports': 'https://github.com/geoelements/LearnMPM/issues',
        'Source': 'https://github.com/geoelements/LearnMPM',
        'Docs': 'https://LearnMPM.readthedocs.io/en/latest/?badge=latest',
    },
)
