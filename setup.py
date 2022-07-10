from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='eudract-py',
      version='1.2.0',
      description='Eudract-py is a Python library for searching clinical trials on EUDRACT',
      url='http://github.com/PaulinCharliquart/eudract-py',
      author='Paulin Charliquart',
      author_email='paulincharliquart@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['eudract'],
      project_urls={
          "Bug Tracker": "https://github.com/PaulinCharliquart/eudract-py/issues",
      },
      classifiers={
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Healthcare Industry",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Bio-Informatics"
      },
      install_requires=[
          'requests', 'bs4'
      ],
      include_package_data=True,
      zip_safe=False
      )
