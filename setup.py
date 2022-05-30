from setuptools import setup


setup(
    name="recon",
    version=0.1,
    description="Collection of recon scripts",
    author="Igor 'hostile' Wojciechowski",
    author_email="igorxwojciechowski@gmail.com",
    install_requires=[
        'psutil==5.8.0'
    ],
    packages=[
        'recon',
        'recon.utils'
    ],
    entry_points = {
        'console_scripts': [
            'recon_aquatone=recon.recon_aquatone:main',
            'recon_content_discovery=recon.recon_content_discovery:main',
            'recon_probe=recon.recon_probe:main',
            'recon_subenum=recon.recon_subenum:main'
        ]
    }
)