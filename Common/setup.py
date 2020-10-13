from setuptools import setup, find_packages

with open("README.md") as f:
    longDescr = f.read()

setup(
    name='premier_eye_common',
    version='0.3',
    packages=find_packages(),
    author='Alex Yurev',
    author_email='sapfir999999@yandex.ru',
    license='MIT',

    long_description=longDescr,
    url='https://github.com/Sapfir0/premier-eye',
    keywords='premier-eye',
)