"""Install package."""
from setuptools import setup, find_packages
setup(
    name='covid_detector',
    version='0.0.1',
    description=(
        'Keras implementation of COVID detection models from medical images'
    ),
    long_description=open('README.md').read(),
    url='https://github.com/jannisborn/medimg_covid_detecter',
    author='Jannis Born',
    author_email='jannis.born@gmx.de',
    install_requires=[
        'numpy', 'tensorflow', 'scikit-learn', 'matplotlib', 'imutils',
        'opencv-contrib-python'
    ],
    packages=find_packages('.'),
    zip_safe=False,
)
