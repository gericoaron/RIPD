try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "Illegal Parking Detection",
    "author": "educational purpose",
    "url": "https://github.com",
    "download_url": "https://github.com",
    "version": "1",
    "install_requires": ["cv2", "numpy", "yml"],
    "packages": ["Illegal_Parking"],
    "scripts": [],
    "name": "RPID"
}

setup(**config)
