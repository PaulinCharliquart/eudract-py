import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='eudract',
      version='0.1',
      description='Find clinical trials info on EUDRACT',
      url='http://github.com/PaulinCharliquart/eudract-py',
      author='Paulin Charliquart',
      author_email='paulincharliquart@gmail.com',
      description="A sample package to qury EUDRACT website",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['eudract-py'],
      project_urls={
        "Bug Tracker": "https://github.com/PaulinCharliquart/eudract-py/issues",
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
      ],
      install_requires=[
          'requests',
      ],
      include_package_data=True,
      zip_safe=False)
