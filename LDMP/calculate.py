# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LDMP - A QGIS plugin
 This plugin supports monitoring and reporting of land degradation to the UNCCD 
 and in support of the SDG Land Degradation Neutrality (LDN) target.
                              -------------------
        begin                : 2017-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Conservation International
        email                : trends.earth@conservation.org
 ***************************************************************************/
"""

import os
import json

from PyQt4 import QtGui
from PyQt4.QtCore import QTextCodec, QSettings, pyqtSignal, QCoreApplication

from qgis.core import QgsGeometry, QgsJSONUtils, QgsVectorLayer, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QGis

from LDMP import log
from LDMP.gui.DlgCalculate import Ui_DlgCalculate as UiDialog
from LDMP.gui.WidgetSelectArea import Ui_WidgetSelectArea
from LDMP.download import read_json, get_admin_bounds


def tr(t):
    return QCoreApplication.translate('LDMPPlugin', t)

class AOI(object):
    def __init__(self, f=None, geojson=None, datatype='polygon'):
        """
        Can initialize with either a file, or a geojson. Note datatype is 
        ignored unless geojson is used.
        """
        self.isValid = False

        if f and not geojson:
            l = QgsVectorLayer(f, "calculation boundary", "ogr")
            log("Geom type: {}, {}".format(l.geometryType(), QGis.Polygon))
            if not l.isValid():
                return
            if l.geometryType() == QGis.Polygon:
                datatype = "polygon"
            elif l.geometryType() == QGis.Point:
                datatype = "point"
            else:
                QtGui.QMessageBox.critical(None, tr("Error"),
                        tr("Failed to process area of interest - unknown geometry type:{}".format(l.geometryType())))
                log("Failed to process area of interest - unknown geometry type.")
                return
        elif not f and geojson:
            l = QgsVectorLayer("{}?crs=epsg:4326".format(datatype), "calculation boundary", "memory")
            fields = QgsJSONUtils.stringToFields(json.dumps(geojson), QTextCodec.codecForName('UTF8'))
            features = QgsJSONUtils.stringToFeatureList(json.dumps(geojson), fields, QTextCodec.codecForName('UTF8'))
            ret = l.dataProvider().addFeatures(features)
            l.commitChanges()
            if not ret:
                QtGui.QMessageBox.critical(None, tr("Error"),
                                           tr("Failed to add geojson to temporary layer."))
                log("Failed to add geojson to temporary layer.")
                return
            l.commitChanges()
        else:
            raise ValueError("Must specify file or geojson")

        crs_source = l.crs()
        crs_dest = QgsCoordinateReferenceSystem(4326)
        t = QgsCoordinateTransform(crs_source, crs_dest)

        # Transform layer to WGS84
        l_wgs84 = QgsVectorLayer("{}?crs=epsg:4326".format(datatype), "calculation boundary (wgs84)",  "memory")
        #CRS transformation
        feats = []
        for f in l.getFeatures():
            g = f.geometry()
            g.transform(t)
            f.setGeometry(g)
            feats.append(f)
        l_wgs84.dataProvider().addFeatures(feats)
        l_wgs84.commitChanges()
        if not l_wgs84.isValid():
            self.layer = None
            log("Error transforming AOI coordinates to WGS84")
            return
        else:
            self.layer = l_wgs84

        # Transform bounding box to WGS84
        self.bounding_box_geom = QgsGeometry.fromRect(l_wgs84.extent())
        # Save a geometry of the bounding box
        self.bounding_box_geom.transform(t)
        # Also save a geojson of the bounding box (needed for shipping to GEE)
        self.bounding_box_geojson = json.loads(self.bounding_box_geom.exportToGeoJSON())

        # Check the coordinates of the bounding box are now in WGS84 (in case 
        # no transformation was available for the chosen coordinate systems)
        bbox = self.bounding_box_geom.boundingBox()
        log("Bounding box: {}, {}, {}, {}".format(bbox.xMaximum(), bbox.xMinimum(), bbox.yMinimum(), bbox.yMinimum()))
        if (bbox.xMinimum() < -180) or \
           (bbox.xMaximum() > 180) or \
           (bbox.yMinimum() < -90) or \
           (bbox.yMinimum() > 90):
            QtGui.QMessageBox.critical(None, tr("Error"),
                                       tr("Coordinates of area of interest could not be transformed to WGS84. Check that the projection system is defined."), None)
            log("Error transforming AOI coordinates to WGS84")
        else:
            self.isValid = True


class AreaWidget(QtGui.QWidget, Ui_WidgetSelectArea):
    def __init__(self, parent=None):
        super(AreaWidget, self).__init__(parent)

        self.setupUi(self)


class DlgCalculate(QtGui.QDialog, UiDialog):
    def __init__(self, parent=None):
        super(DlgCalculate, self).__init__(parent)

        self.setupUi(self)

        self.dlg_calculate_prod = DlgCalculateProd()
        self.dlg_calculate_lc = DlgCalculateLC()
        self.dlg_calculate_soc = DlgCalculateSOC()

        self.btn_prod.clicked.connect(self.btn_prod_clicked)
        self.btn_lc.clicked.connect(self.btn_lc_clicked)
        self.btn_soc.clicked.connect(self.btn_soc_clicked)

    def btn_prod_clicked(self):
        self.close()
        result = self.dlg_calculate_prod.exec_()

    def btn_lc_clicked(self):
        self.close()
        result = self.dlg_calculate_lc.exec_()

    def btn_soc_clicked(self):
        self.close()
        result = self.dlg_calculate_soc.exec_()


class DlgCalculateBase(QtGui.QDialog):
    """Base class for individual indicator calculate dialogs"""
    firstShowEvent = pyqtSignal()

    def __init__(self, parent=None):
        super(DlgCalculateBase, self).__init__(parent)

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'data', 'scripts.json')) as script_file:
            self.scripts = json.load(script_file)

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'data', 'gee_datasets.json')) as datasets_file:
            self.datasets = json.load(datasets_file)

        self._firstShowEvent = True
        self.reset_tab_on_showEvent = True

        self.firstShowEvent.connect(self.firstShow)

    def showEvent(self, event):
        super(DlgCalculateBase, self).showEvent(event)

        if self._firstShowEvent:
            self._firstShowEvent = False
            self.firstShowEvent.emit()

        if self.reset_tab_on_showEvent:
            self.TabBox.setCurrentIndex(0)

    def firstShow(self):
        self.area_tab = AreaWidget()
        self.TabBox.addTab(self.area_tab, self.tr('Area'))

        # Add the area selector tab
        self.button_calculate.clicked.connect(self.btn_calculate)
        self.button_prev.clicked.connect(self.tab_back)
        self.button_next.clicked.connect(self.tab_forward)

        # Start on first tab so button_prev and calculate should be disabled
        self.button_prev.setEnabled(False)
        self.button_calculate.setEnabled(False)
        self.TabBox.currentChanged.connect(self.tab_changed)

        self.setup_area_selection()

    def tab_back(self):
        if self.TabBox.currentIndex() - 1 >= 0:
            self.TabBox.setCurrentIndex(self.TabBox.currentIndex() - 1)

    def tab_forward(self):
        if self.TabBox.currentIndex() + 1 < self.TabBox.count():
            self.TabBox.setCurrentIndex(self.TabBox.currentIndex() + 1)

    def tab_changed(self):
        if self.TabBox.currentIndex() > 0:
            self.button_prev.setEnabled(True)
        else:
            self.button_prev.setEnabled(False)

        if self.TabBox.currentIndex() < (self.TabBox.count() - 1):
            self.button_next.setEnabled(True)
        else:
            self.button_next.setEnabled(False)

        if self.TabBox.currentIndex() == (self.TabBox.count() - 1):
            self.button_calculate.setEnabled(True)
        else:
            self.button_calculate.setEnabled(False)

    def btn_cancel(self):
        self.close()

    def setup_area_selection(self):
        self.admin_bounds_key = get_admin_bounds()
        if not self.admin_bounds_key:
            raise ValueError('Admin boundaries not available')

        self.area_tab.area_admin_0.addItems(sorted(self.admin_bounds_key.keys()))
        self.populate_admin_1()

        self.area_tab.area_admin_0.currentIndexChanged.connect(self.populate_admin_1)

        self.area_tab.area_fromfile_browse.clicked.connect(self.open_shp_browse)
        self.area_tab.area_admin.toggled.connect(self.area_admin_toggle)
        self.area_tab.area_fromfile.toggled.connect(self.area_fromfile_toggle)

    def load_admin_polys(self):
        adm0_a3 = self.admin_bounds_key[self.area_tab.area_admin_0.currentText()]['code']
        admin_polys = read_json('admin_bounds_polys_{}.json.gz'.format(adm0_a3), verify=False)
        if not admin_polys:
            return None
        if not self.area_tab.area_admin_1.currentText() or self.area_tab.area_admin_1.currentText() == 'All regions':
            return admin_polys['geojson']
        else:
            admin_1_code = self.admin_bounds_key[self.area_tab.area_admin_0.currentText()]['admin1'][self.area_tab.area_admin_1.currentText()]['code']
            return admin_polys['admin1'][admin_1_code]['geojson']

    def area_admin_toggle(self):
        if self.area_tab.area_admin.isChecked():
            self.area_tab.area_admin_0.setEnabled(True)
            self.area_tab.area_admin_1.setEnabled(True)
        else:
            self.area_tab.area_admin_0.setEnabled(False)
            self.area_tab.area_admin_1.setEnabled(False)

    def area_fromfile_toggle(self):
        if self.area_tab.area_fromfile.isChecked():
            self.area_tab.area_fromfile_file.setEnabled(True)
            self.area_tab.area_fromfile_browse.setEnabled(True)
        else:
            self.area_tab.area_fromfile_file.setEnabled(False)
            self.area_tab.area_fromfile_browse.setEnabled(False)

    def open_shp_browse(self):
        shpfile = QtGui.QFileDialog.getOpenFileName(self,
                                                    self.tr('Select a file defining the area of interst'),
                                                    QSettings().value("LDMP/area_file_dir", None),
                                                    self.tr('Spatial file (*.*)'))
        if os.access(shpfile, os.R_OK):
            QSettings().setValue("LDMP/area_file_dir", os.path.dirname(shpfile))
        self.area_tab.area_fromfile_file.setText(shpfile)

    def populate_admin_1(self):
        self.area_tab.area_admin_1.clear()
        self.area_tab.area_admin_1.addItems(['All regions'])
        self.area_tab.area_admin_1.addItems(sorted(self.admin_bounds_key[self.area_tab.area_admin_0.currentText()]['admin1'].keys()))

    def btn_calculate(self):
        if self.area_tab.area_admin.isChecked():
            if not self.area_tab.area_admin_0.currentText():
                QtGui.QMessageBox.critical(None, self.tr("Error"),
                                           self.tr("Choose a first level administrative boundary."), None)
                return False
            self.button_calculate.setEnabled(False)
            geojson = self.load_admin_polys()
            self.button_calculate.setEnabled(True)
            if not geojson:
                QtGui.QMessageBox.critical(None, self.tr("Error"),
                                           self.tr("Unable to load administrative boundaries."), None)
                return False
            self.aoi = AOI(geojson=geojson)
        elif self.area_tab.area_fromfile.isChecked():
            if not self.area_tab.area_fromfile_file.text():
                QtGui.QMessageBox.critical(None, self.tr("Error"),
                                           self.tr("Choose a file to define the area of interest."), None)
                return False
            self.aoi = AOI(f=self.area_tab.area_fromfile_file.text())
        else:
            self.aoi = None

        if self.aoi and not self.aoi.isValid:
            QtGui.QMessageBox.critical(None, self.tr("Error"),
                                       self.tr("Unable to read area file."), None)
            return False

        return True


from LDMP.calculate_prod import DlgCalculateProd
from LDMP.calculate_lc import DlgCalculateLC
from LDMP.calculate_soc import DlgCalculateSOC
