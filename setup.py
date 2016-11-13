from setuptools import setup, find_packages

setup(name='ds',
      version='0.1',
      description='Synology Download Station API',
      url='https://bitbucket.org/ltekieli/ds',
      author='Lukasz Tekieli',
      author_email='mail@ltekieli.com',
      license='MIT',
      packages=find_packages(),
      scripts=['bin/synods'],
      zip_safe=False)
