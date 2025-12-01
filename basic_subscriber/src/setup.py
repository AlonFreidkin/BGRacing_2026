from setuptools import find_packages, setup

package_name = 'basic_subscriber'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pandas', 'numpy', 'matplotlib', 'scipy'],
    zip_safe=True,
    maintainer='edward-grieg',
    maintainer_email='alon3492xd@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'subscriber_s = basic_subscriber.subscriber_s:main'
        ],
    },
)
