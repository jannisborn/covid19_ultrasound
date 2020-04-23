"""Install package."""
from setuptools import setup, find_packages
setup(
    name='pocovidnet',
    version='0.0.1',
    description=(
        'Keras implementation of COVID19 detection models from POCUS data'
    ),
    long_description=open('README.md').read(),
    url='https://github.com/jannisborn/medimg_covid_detecter',
    author='Jannis Born',
    author_email='jannis.born@gmx.de',
    install_requires=[
        'numpy', 'tensorflow', 'scikit-learn', 'matplotlib', 'imutils',
        'opencv-contrib-python', 'flask'
    ],
    packages=find_packages('.'),
    zip_safe=False,
)
