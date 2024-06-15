from setuptools import setup, find_packages

setup(
    name='vtpass-python-sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'annotated-types==0.7.0',
        'certifi==2024.6.2',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        'pydantic==2.7.4',
        'pydantic-core==2.18.4',
        'python-decouple==3.8',
        'python-dotenv==1.0.1',
        'pytz==2024.1',
        'requests==2.32.3',
        'typing-extensions==4.12.2',
        'urllib3==2.2.1',
    ],
    author='Abiola Adeshina',
    author_email='abiolaadedayo1993@gmail.com',
    description='VTPass Python SDK to interact with various services provided by VTPass. The SDK allows you to perform operations such as checking wallet balance, purchasing airtime, and subscribing to data services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Abiorh001/vtpass-pythonsdk.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
