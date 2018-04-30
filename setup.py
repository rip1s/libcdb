# Author: nonick

from setuptools import setup

try:
    from pypandoc import convert_file

    long_description = convert_file('README.md', 'md')

except ImportError:
    long_description = """
    Yet another libc search library based on https://libc.ml/

    Useful in some pwn challenge which without libc provided.

    More information at: https://github.com/unamer/libcdb.
"""

setup(name='libcdb',
      description='A libc search utility based on https://libc.ml/',
      long_description=long_description,
      version='0.1',
      url='https://github.com/unamer/libcdb',
      author='nonick',
      author_email='n0nick@protonmail.com',
      license='GNU LGPLv3',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ],
      packages=['libcdb'],
      install_requires=[
          'requests'
      ])
