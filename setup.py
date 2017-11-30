from setuptools import setup

setup(name='neucogar',
      version='0.0.1',
      description='',
      url='https://github.com/research-team/neucogar-lib',
      author='research-team but mostly Panzerwaffe',
      author_email='research-team@github.com',
      license='MIT',
      packages=['neucogar'],
      install_requires=[
          'numpy',
          'seaborn',
          'matplotlib',
      ],
      zip_safe=False)