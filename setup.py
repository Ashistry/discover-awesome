# setup.py
from setuptools import setup, find_packages

# Read requirements from requirements.txt
def read_requirements(file_path):
    with open(file_path, 'r') as f:
        # Strip whitespace and ignore comments
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
requirements = read_requirements('requirements.txt')

setup(
    name='discover_awesome',
    version='0.0.0',
    packages=find_packages(), 
    install_requires= requirements,
    entry_points={
        'console_scripts': [
            'discover-awesome=discover_awesome.main:main',  
        ],
    },
    author='ashistry',
    author_email='ashistry@proton.me',
    description='A CLI tool to explore all (a lot of, not actually all) lists in the awesome-list Github topic.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ashistry/discover_awesome',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
