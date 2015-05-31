#!/usr/bin/env python
#--!-- coding: utf8 --!--
 
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui.mainWindow import *
from loadSave import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.readSettings()
        
        # UI
        self.splitterPersos.setStretchFactor(0, 25)
        self.splitterPersos.setStretchFactor(1, 75)
        
        self.splitterPlot.setStretchFactor(0, 20)
        self.splitterPlot.setStretchFactor(1, 40)
        self.splitterPlot.setStretchFactor(2, 40)
        
        
        self.splitterPlan.setStretchFactor(0, 25)
        self.splitterPlan.setStretchFactor(1, 75)
        
        
        self.splitterRedac.setStretchFactor(0, 20)
        self.splitterRedac.setStretchFactor(1, 60)
        self.splitterRedac.setStretchFactor(2, 20)
        
        
        # Signals
        self.tabMain.currentChanged.connect(self.updateTabMain)
        
        # Word count
        self.mprWordCount = QSignalMapper(self)
        for t, i in [
            (self.txtSummarySentance, 0),
            (self.txtSummaryPara, 1),
            (self.txtSummaryPage, 2),
            (self.txtSummaryFull, 3)
            ]:
            t.textChanged.connect(self.mprWordCount.map)
            self.mprWordCount.setMapping(t, i)
        self.mprWordCount.mapped.connect(self.wordCount)
        
        # Snowflake Method Cycle
        self.mapperCycle = QSignalMapper(self)
        for t, i in [
            (self.btnStepTwo,   0),
            (self.btnStepThree, 1),
            (self.btnStepFour,  2),
            (self.btnStepFive,  3),
            (self.btnStepSix,   4),
            (self.btnStepSeven, 5),
            (self.btnStepEight, 6)
            ]:
            t.clicked.connect(self.mapperCycle.map)
            self.mapperCycle.setMapping(t, i)
            
        self.mapperCycle.mapped.connect(self.clickCycle)
        
        
        # Données
        self.mdlFlatData = QStandardItemModel(2, 8)
        self.tblDebugFlatData.setModel(self.mdlFlatData)
        
        self.mprSummary = QDataWidgetMapper()
        self.mprSummary.setModel(self.mdlFlatData)
        self.mprSummary.addMapping(self.txtSummarySentance, 0)
        self.mprSummary.addMapping(self.txtSummarySentance_2, 0)
        self.mprSummary.addMapping(self.txtSummaryPara, 1)
        self.mprSummary.addMapping(self.txtSummaryPara_2, 1)
        self.mprSummary.addMapping(self.txtPlotSummaryPara, 1)
        self.mprSummary.addMapping(self.txtSummaryPage, 2)
        self.mprSummary.addMapping(self.txtSummaryPage_2, 2)
        self.mprSummary.addMapping(self.txtPlotSummaryPage, 2)
        self.mprSummary.addMapping(self.txtSummaryFull, 3)
        self.mprSummary.addMapping(self.txtPlotSummaryFull, 3)
        self.mprSummary.setCurrentIndex(1)
        
        self.mprInfos = QDataWidgetMapper()
        self.mprInfos.setModel(self.mdlFlatData)
        self.mprInfos.addMapping(self.txtGeneralTitle, 0)
        self.mprInfos.addMapping(self.txtGeneralSubtitle, 1)
        self.mprInfos.addMapping(self.txtGeneralSerie, 2)
        self.mprInfos.addMapping(self.txtGeneralVolume, 3)
        self.mprInfos.addMapping(self.txtGeneralGenre, 4)
        self.mprInfos.addMapping(self.txtGeneralLicense, 5)
        self.mprInfos.addMapping(self.txtGeneralAuthor, 6)
        self.mprInfos.addMapping(self.txtGeneralEmail, 7)
        self.mprInfos.setCurrentIndex(0)
        
        # Persos
        self.mdlPersos = QStandardItemModel(0, 10)
        self.mdlPersosInfos = QStandardItemModel(3, 0)
        self.mdlPersosInfos.insertColumn(0, [QStandardItem(i) for i in ["Date de naissance", "Àge", "Animal favori"]])
        self.mdlPersosInfos.setHorizontalHeaderLabels(["Description"])
        self.lstPersos.setModel(self.mdlPersos)
        self.tblDebugPersos.setModel(self.mdlPersos)
        self.tblPersoInfos.setModel(self.mdlPersosInfos)
        #self.tblPersoInfos.horizontalHeader().setStretchLastSection(True)
        #self.tblPersoInfos.horizontalHeader().hide()
        self.tblDebugPersosInfos.setModel(self.mdlPersosInfos)
        
        self.btnAddPerso.clicked.connect(self.createPerso)
        self.btnRmPerso.clicked.connect(self.removePerso)
        self.btnPersoAddInfo.clicked.connect(lambda: self.mdlPersosInfos.insertRow(self.mdlPersosInfos.rowCount()))
        self.mprPersos = QDataWidgetMapper()
        self.mprPersos.setModel(self.mdlPersos)
        
        mapping = [
            self.txtPersoName,
            self.txtPersoMotivation,
            self.txtPersoGoal,
            self.txtPersoConflict,
            self.txtPersoEpiphany,
            self.txtPersoSummarySentance,
            self.txtPersoSummaryPara,
            self.txtPersoSummaryFull,
            ]
        for w in mapping:
                self.mprPersos.addMapping(w, mapping.index(w))    
        self.mprPersos.addMapping(self.sldPersoImportance, 8, "importance")
        self.sldPersoImportance.importanceChanged.connect(self.mprPersos.submit)
            
        self.mprPersos.setCurrentIndex(0)
        self.lstPersos.selectionModel().currentChanged.connect(self.mprPersos.setCurrentModelIndex)
        self.lstPersos.selectionModel().currentChanged.connect(self.changeCurrentPerso)
        
        #Debug
        self.mdlFlatData.setVerticalHeaderLabels(["Infos générales", "Summary"])
        self.tblDebugFlatData.setModel(self.mdlFlatData)
        
        
        self.loadProject("test_project")
        
        
    def loadProject(self, project):
        self.currentProject = project
        loadStandardItemModelXML(self.mdlFlatData, "{}/flatModel.xml".format(project))
        loadStandardItemModelXML(self.mdlPersos, "{}/perso.xml".format(project))
        loadStandardItemModelXML(self.mdlPersosInfos, "{}/persoInfos.xml".format(project))
        
        
    def createPerso(self):
        p = QStandardItem("Nouveau perso")
        self.mdlPersos.appendRow(p) 
        #self.mdlPersosInfos.appendColumn([QStandardItem()]*self.mdlPersosInfos.columnCount())
        self.mdlPersosInfos.insertColumn(self.mdlPersosInfos.columnCount())
        self.mdlPersosInfos.setHorizontalHeaderItem(self.mdlPersosInfos.columnCount()-1, QStandardItem("Valeur"))
        
    def removePerso(self):
        i = self.lstPersos.currentIndex()
        self.mdlPersos.takeRow(i.row())
        self.mdlPersosInfos.takeColumn(i.row()+1)
        
    def changeCurrentPerso(self):
        for i in range(self.mdlPersosInfos.columnCount()):
            self.tblPersoInfos.setColumnHidden(i, i<>0 and i<>self.lstPersos.currentIndex().row()+1)
        #self.tblPersoInfos.horizontalHeader().resizeSections(QHeaderView.Stretch)
        
    def readSettings(self):
        # Load State and geometry
        settings = QSettings(qApp.organizationName(), qApp.applicationName())
        self.restoreGeometry(settings.value("geometry").toByteArray())
        self.restoreState(settings.value("windowState").toByteArray())
        
    def closeEvent(self, event):
        # Save State and geometry
        settings = QSettings(qApp.organizationName(), qApp.applicationName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        
        # Save data from models
        saveStandardItemModelXML(self.mdlFlatData, "{}/flatModel.xml".format(self.currentProject))
        saveStandardItemModelXML(self.mdlPersos, "{}/perso.xml".format(self.currentProject))
        saveStandardItemModelXML(self.mdlPersosInfos, "{}/persoInfos.xml".format(self.currentProject))
        
        
        # closeEvent
        QMainWindow.closeEvent(self, event)
        
    def updateTabMain(self, tab):
        if tab == 3:  # Plot 
            self.txtPlotSummaryPara.setPlainText(self.txtSummaryPara.toPlainText())
            self.txtPlotSummaryPage.setPlainText(self.txtSummaryPage.toPlainText())
            self.txtPlotSummaryFull.setPlainText(self.txtSummaryFull.toPlainText())
        
    def clickCycle(self, i):
        if i == 0: # step 2 - paragraph summary
            self.tabMain.setCurrentIndex(1)
            self.tabSummary.setCurrentIndex(1)
        if i == 1: # step 3 - characters summary
            self.tabMain.setCurrentIndex(2)
            self.tabPersos.setCurrentIndex(0)
        if i == 2: # step 4 - page summary
            self.tabMain.setCurrentIndex(1)
            self.tabSummary.setCurrentIndex(2)
        if i == 3: # step 5 - characters description
            self.tabMain.setCurrentIndex(2)
            self.tabPersos.setCurrentIndex(1)
        if i == 4: # step 6 - four page synopsis
            self.tabMain.setCurrentIndex(1)
            self.tabSummary.setCurrentIndex(3)
        if i == 5: # step 7 - full character charts
            self.tabMain.setCurrentIndex(2)
            self.tabPersos.setCurrentIndex(2)
        if i == 6: # step 8 - scene list
            self.tabMain.setCurrentIndex(3)
        
            
        
    "Updates word counts over tabs"
    def wordCount(self, i):
        
        src= {
            0:self.txtSummarySentance,
            1:self.txtSummaryPara,
            2:self.txtSummaryPage,
            3:self.txtSummaryFull
            }[i]
        
        lbl = {
            0:self.lblSummaryWCSentance,
            1:self.lblSummaryWCPara,
            2:self.lblSummaryWCPage,
            3:self.lblSummaryWCFull
            }[i]
        
        wc = len(src.toPlainText().trimmed().split(" ")) if src.toPlainText() else 0
        if i in [2, 3]: pages = " (~{} pages)".format(int(wc / 25) / 10.)
        else: pages = ""
        lbl.setText("Mots: {}{}".format(wc, pages))