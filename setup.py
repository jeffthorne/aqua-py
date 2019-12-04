from setuptools import setup

setup(name='aqua',
      version='0.1.6',
      description='Python 3 client for Aqua\'s CSP Platform',
      url='https://github.com/',
      author='Jeff Thorne',
      author_email='jthorne@u.washington.edu',
      license='MIT',
      packages=['aqua'],
      install_requires=['requests == 2.22.0'],
      zip_safe=False,)

