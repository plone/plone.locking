from setuptools import setup, find_packages
import sys, os

version = '2.0'

setup(name='plone.locking',
      version=version,
      description="webdav locking support",
      long_description="""\
plone.locking provides WebDAV locking support, with useful abstractions and
views to assist a user interface. By default, it provides "stealable" locks,
but can support other lock types. It is used by Plone, Archetypes and
plone.app.iterate.
""",
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='locking webdav plone archetypes',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.locking',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.Archetypes',
            'Products.PloneTestCase',
        ]
      ),
      install_requires=[
        'setuptools',
        'ZODB3',
        'zope.annotation',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.viewlet',
        # 'Acquisition',
        # 'DateTime',
        # 'Zope2',
      ],
      )
