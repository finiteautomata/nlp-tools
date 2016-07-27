from setuptools import setup

setup(name='nlp-tools',
      version='0.1',
      description='NLP examples in Python',
      url='http://github.com/finiteautomata/nlp-tools',
      author='Juan Manuel Perez',
      author_email='jmperez.85@gmail.com',
      license='MIT',
      install_requires=[
          'numpy',
      ],
      test_suite="tests",
      packages=['nlptools'],
      zip_safe=False)