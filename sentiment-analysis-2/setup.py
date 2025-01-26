from setuptools import setup, find_packages

setup(
    name='sentiment-analysis-2',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A sentiment analysis project',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
)