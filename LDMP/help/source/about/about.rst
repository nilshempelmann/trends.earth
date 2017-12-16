﻿About
=====

|trends.earth| was produced as part of the project "Enabling the use of global 
data sources to assess and monitor land degradation at multiple scales", funded 
by the Global Environment Facility.

Contacting the team
-------------------

Contact the `trends.earth <mailto:trends.earth@conservation.org>`_ team with 
any comments or suggestions. If you have specific bugs to report or 
improvements to the tool that you would like to suggest, you can also submit 
them in the `issue tracker on Github 
<https://github.com/ConservationInternational/trends.earth/issues>`_ for 
|trends.earth|.

Authors
-------

Contributors to the documentation and |trends.earth| include Yengoh Genesis 
[1]_, Mariano Gonzalez-Roglich [2]_, Monica Noon [2]_, Lennart Olsson [1]_, 
Tristan Schnader [2]_, Anna Tengberg [1]_, and Alex Zvoleff [2]_.

The Land Degradation Monitoring Project is a partnership of Conservation 
International, Lund University, and the National Aeronautics and Space 
Administration (NASA), and is funded by the Global Environment Facility (GEF).

.. |logoCI| image:: /static/common/logo_CI_square.png
    :width: 150
    :target: http://www.conservation.org
.. |logoLund| image:: /static/common/logo_Lund_square.png
    :width: 125
    :target: http://www.lunduniversity.lu.se
.. |logoNASA| image:: /static/common/logo_NASA_square.png
    :width: 125
    :target: http://www.nasa.gov
.. |logoGEF| image:: /static/common/logo_GEF.png
    :width: 125
    :target: https://www.thegef.org

.. table::
    :align: center
    :widths: grid

    ======== ========== ========== =========
    |logoCI| |logoLund| |logoNASA| |logoGEF|
    ======== ========== ========== =========

.. [1] `Lund University <http://www.lunduniversity.lu.se>`_
.. [2] `Conservation International <http://www.conservation.org>`_

|trends.earth| uses `Google Earth Engine <https://earthengine.google.com>`_ to 
compute indicators in the cloud.

.. image:: /static/common/logo_earth_engine.png
    :align: center
    :width: 250
    :target: https://earthengine.google.com

Acknowledgements
----------------

workshop participants in TZA

Neil Sims, Sasha Alexander, Renato Cumani, John Wasige, Sara Minelli

CSA participants


Data sources
------------

|trends.earth| draws on a number of data sources. The data sets listed below are 
owned/made available by the following organizations and individuals under 
separate terms as indicated in their respective metadata.

NDVI
~~~~

+------------------+-----------+---------+--------+---------+
| Sensor/Dataset   | Temporal  | Spatial | Extent | License |
+==================+===========+=========+========+=========+
| `AVHRR/GIMMS`_   | 1982-2015 | 8 km    | Global |         |
+------------------+-----------+---------+--------+---------+
| `MOD13Q1-coll6`_ | 2001-2016 | 250 m   | Global |         |
+------------------+-----------+---------+--------+---------+

.. _AVHRR/GIMMS: https://glam1.gsfc.nasa.gov/
.. _MOD13Q1-coll6:
   https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod13q1_v006

Soil moisture
~~~~~~~~~~~~~

+----------------+-----------+---------------+--------+---------+
| Sensor/Dataset | Temporal  | Spatial       | Extent | License |
+================+===========+===============+========+=========+
| `MERRA 2`_     | 1980-2016 | 0.5° x 0.625° | Global |         |
+----------------+-----------+---------------+--------+---------+
| `ERA I`_       | 1979-2016 | 0.75° x 0.75° | Global |         |
+----------------+-----------+---------------+--------+---------+

.. _MERRA 2: https://gmao.gsfc.nasa.gov/reanalysis/MERRA-Land
.. _ERA I: 
   https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim-land

Precipitation
~~~~~~~~~~~~~

+----------------------+-----------+-------------+---------+---------+
| Sensor/Dataset       | Temporal  | Spatial     | Extent  | License |
+======================+===========+=============+=========+=========+
| `GPCP v2.3 1 month`_ | 1979-2016 | 2.5° x 2.5° | Global  |         |
+----------------------+-----------+-------------+---------+---------+
| `GPCC V7`_           | 1901-2016 | 1° x 1°     | Global  |         |
+----------------------+-----------+-------------+---------+---------+
| `CHIRPS`_            | 1981-2016 | 5 km        | 50N-50S |         |
+----------------------+-----------+-------------+---------+---------+
| `PERSIANN-CDR`_      | 1983-2015 | 25 km       | 60N-60S |         |
+----------------------+-----------+-------------+---------+---------+

.. _GPCP v2.3 1 month: https://www.esrl.noaa.gov/psd/data/gridded/data.gpcp.html
.. _GPCC V7: https://www.esrl.noaa.gov/psd/data/gridded/data.gpcc.html
.. _CHIRPS:  http://chg.geog.ucsb.edu/data/chirps
.. _PERSIANN-CDR: http://chrsdata.eng.uci.edu

Evapotranspiration
~~~~~~~~~~~~~~~~~~

+----------------+-----------+---------+--------+---------+
| Sensor/Dataset | Temporal  | Spatial | Extent | License |
+================+===========+=========+========+=========+
| MOD16A2_       | 2000-2014 | 1 km    | Global |         |
+----------------+-----------+---------+--------+---------+

.. _MOD16A2:
   https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod16a2_v006

Land cover
~~~~~~~~~~

+-----------------------+-----------+---------+--------+---------+
| Sensor/Dataset        | Temporal  | Spatial | Extent | License |
+=======================+===========+=========+========+=========+
| `ESA CCI Land Cover`_ | 1992-2015 | 300 m   | Global |         |
+-----------------------+-----------+---------+--------+---------+

.. _ESA CCI Land Cover: https://www.esa-landcover-cci.org/


Soil carbon
~~~~~~~~~~~

+-----------------------+----------+---------+--------+---------+
| Sensor/Dataset        | Temporal | Spatial | Extent | License |
+=======================+==========+=========+========+=========+
| `Soil Grids (ISRIC)`_ | Present  | 250 m   | Global |         |
+-----------------------+----------+---------+--------+---------+

.. _Soil Grids (ISRIC): https://www.soilgrids.org/

Agroecological Zones
~~~~~~~~~~~~~~~~~~~~

+---------------------------------------------------+----------+---------+--------+---------+
| Sensor/Dataset                                    | Temporal | Spatial | Extent | License |
+===================================================+==========+=========+========+=========+
| `FAO - IIASA Global Agroecological Zones (GAEZ)`_ | 2000     | 8 km    | Global |         |
+---------------------------------------------------+----------+---------+--------+---------+

.. _FAO - IIASA Global Agroecological Zones (GAEZ): http://www.fao.org/nr/gaez/en

License
-------

|trends.earth| is free and open-source. It is licensed under the `GNU General 
Public License, version 2.0 or later 
<https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>`_.

This site and the products of |trends.earth| are made available under the terms 
of the `Creative Commons Attribution 4.0 International License (CC BY 4.0) 
<https://creativecommons.org/licenses/by/4.0>`_. The boundaries and names used, 
and the designations used, in |trends.earth| do not imply official endorsement or 
acceptance by Conservation International Foundation, or its partner 
organizations and contributors. 