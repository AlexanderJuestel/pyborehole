.. _about_ref:

About
=====

PyBorehole is an open-source Python package for processing borehole data. It is similar to the `welly <https://code.agilescientific.com/welly/>`_ but aims at extending the functionality of welly to make working will borehole data even easier.

Authors
-------
The following list (sorted by name) shows the authors with substantial contributions to the conception or design of the software. The authors also provided new code or revised existing code and documentation.


* Alexander Jüstel (`@AlexanderJuestel <https://github.com/AlexanderJuestel/>`_)


Resources
---------

* `PyBorehole Documentation <https://pyborehole.readthedocs.io/en/latest/index.html>`_
* `PyBorehole Github Repository <https://github.com/AlexanderJuestel/pyborehole>`_
* `PyBorehole Issue Tracker <https://github.com/AlexanderJuestel/pyborehole/issues>`_
* `PyBorehole Discussion Forum <https://github.com/AlexanderJuestel/pyborehole/discussions>`_
* `PyBorehole on PyPi <https://pypi.org/project/pyborehole/>`_
* `PyBorehole on conda-forge <https://anaconda.org/conda-forge/pyborehole>`_

Citing PyBorehole
------------------
If you are using **PyBorehole** for your scientific research, please remember to cite our work.

.. code::

   @article{Jüstel2024,
    doi = {10.21105/joss.xxxxx},
    url = {https://doi.org/10.21105/joss.xxxxx},
    year = {2024}, publisher = {The Open Journal},
    volume = {x},
    number = {xx},
    pages = {xxxx},
    author = {Alexander Jüstel},
    title = {PyBorehole - Processing Tool for Borehole},
    journal = {Journal of Open Source Software}
    }

* `CITATION.cff <https://github.com/AlexanderJuestel/pyborehole/tree/main/CITATION.cff>`_
* `CITATION.md <https://github.com/AlexanderJuestel/pyborehole/tree/main/CITATION.md>`_

FAIR Principle
--------------

The developers of PyBorehole want to make the API, the tutorials and examples meet and adhere to the FAIR data principles (e.g. `FAIR Principles <https://www.nature.com/articles/sdata201618#:~:text=This%20article%20describes%20four%20foundational,contemporary%2C%20formal%20scholarly%20digital%20publishing.>`_).

**Findable**
With each release, the data stored in the PyBorehole repositories are uploaded to Zenodo where a persistent identifier is provided for each release. The data for the latest release of PyBorehole can be found at `https://zenodo.org/record/ <https://zenodo.org/record/>`_. It is referred to Zenodo as the Github repositories do not strictly fulfill the criteria of having a globally unique and persistent identifier assigned to the (meta)data. However, all code and data can currently be found at `https://github.com/AlexanderJuestel/pyborehole <https://github.com/AlexanderJuestel/pyborehole>`_.

**Accessible**
The files stored in the respective Zenodo repositories can be downloaded without registration as ZIP file. In addition, the data can be downloaded from the aforementioned Github repositories without registration as ZIP files or via `git <https://git-scm.com/>`_. The functionality of PyBorehole can be easily accessed through installing the software using `conda-forge <https://anaconda.org/conda-forge/pyborehole/files>`_ or `pip <https://pypi.org/project/pyborehole/>`_. Please see also the `Installation Instructions <installation>` provided.

**Interoperable**
No commercial software is needed to read or alter the data provided in the repositories. Files containing code can be opened with any text editor, vector and raster data can be opened with open-source software such as `QGIS <https://qgis.org/en/site/>`_ or the respective Python libraries such as GeoPandas or Rasterio. Mesh data can also be opened using text editors or Python packages such as PyVista or open-source software like Blender. We mostly use file formats that are common to the geospatial community (.shp, .tif, ZMAP-Grids, etc.) and that are not proprietary.

**Reusable**
The provision of tutorials, examples and in fact this documentation makes the data provided in the repositories reusable under the license provided below.





License
-------

                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.


This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

0. Additional Definitions.

As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

"The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

1. Exception to Section 3 of the GNU GPL.

You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

2. Conveying Modified Versions.

If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

a) under this License, provided that you make a good faith effort to
ensure that, in the event an Application does not supply the
function or data, the facility still operates, and performs
whatever part of its purpose remains meaningful, or

b) under the GNU GPL, with none of the additional permissions of
this License applicable to that copy.

3. Object Code Incorporating Material from Library Header Files.

The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

a) Give prominent notice with each copy of the object code that the
Library is used in it and that the Library and its use are
covered by this License.

b) Accompany the object code with a copy of the GNU GPL and this license
document.

4. Combined Works.

You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

a) Give prominent notice with each copy of the Combined Work that
the Library is used in it and that the Library and its use are
covered by this License.

b) Accompany the Combined Work with a copy of the GNU GPL and this license
document.

c) For a Combined Work that displays copyright notices during
execution, include the copyright notice for the Library among
these notices, as well as a reference directing the user to the
copies of the GNU GPL and this license document.

d) Do one of the following:

0) Convey the Minimal Corresponding Source under the terms of this
License, and the Corresponding Application Code in a form
suitable for, and under terms that permit, the user to
recombine or relink the Application with a modified version of
the Linked Version to produce a modified Combined Work, in the
manner specified by section 6 of the GNU GPL for conveying
Corresponding Source.

1) Use a suitable shared library mechanism for linking with the
Library.  A suitable mechanism is one that (a) uses at run time
a copy of the Library already present on the user's computer
system, and (b) will operate properly with a modified version
of the Library that is interface-compatible with the Linked
Version.

e) Provide Installation Information, but only if you would otherwise
be required to provide such information under section 6 of the
GNU GPL, and only to the extent that such information is
necessary to install and execute a modified version of the
Combined Work produced by recombining or relinking the
Application with a modified version of the Linked Version. (If
you use option 4d0, the Installation Information must accompany
the Minimal Corresponding Source and Corresponding Application
Code. If you use option 4d1, you must provide the Installation
Information in the manner specified by section 6 of the GNU GPL
for conveying Corresponding Source.)

5. Combined Libraries.

You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

a) Accompany the combined library with a copy of the same work based
on the Library, uncombined with any other library facilities,
conveyed under the terms of this License.

b) Give prominent notice with the combined library that part of it
is a work based on the Library, and explaining where to find the
accompanying uncombined form of the same work.

6. Revised Versions of the GNU Lesser General Public License.

The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.

References
----------

Herbst, E., Khashfe, E., Jüstel, A., Strozyk, F. & Kukla, P., 2021. A Heat Demand Map of North-West Europe – its impact
on supply areas and identification of potential production areas for deep geothermal energy. GeoKarlsruhe 2021,
http://dx.doi.org/10.48380/dggv-j2wj-nk88.

