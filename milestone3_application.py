## Anthony Lam WSU ID#11669440
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "G:\CptS451_milestone2\milestone2_GUI.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1_project(QMainWindow):
    def __init__(self):
        super(milestone1_project, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.CityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.ZipCodeList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.CategoriesList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.clearButton.clicked.connect(self.clearAll)

    
    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='test_milestone2' user='postgres' host='localhost' password='Ss204091'")
        except:
            print('Unable to connect to the database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result
    
    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "Select distinct state from Business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("loadStateList Query failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
    
    def stateChanged(self):
        self.ui.CityList.clear()
        state = self.ui.stateList.currentText()
        if(self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.CityList.addItem(row[0])
            except:
                print("stateChanged Query failed")

    def cityChanged(self):
        self.ui.ZipCodeList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.CityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.CityList.selectedItems()[0].text()
            sql_str = "SELECT distinct zipcode FROM business WHERE city ='" + city + "' ORDER BY zipcode;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.ZipCodeList.addItem(str(row[0]))
            except:
                print("cityChanged Query failed")

    def zipChanged(self):
        self.ui.CategoriesList.clear()
        self.ui.totalpopList.clear()
        self.ui.nobusinessList.clear()
        self.ui.averageIncomeList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.CityList.selectedItems()) > 0) and (len(self.ui.ZipCodeList.selectedItems()) > 0):
            zipCode = self.ui.ZipCodeList.selectedItems()[0].text()
            sql_str = "Select distinct category_name from Business NATURAL JOIN Categories WHERE zipcode='" + zipCode + "' ORDER BY category_name;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.CategoriesList.addItem(row[0])
            except:
                print("zipChanged Query failed")

            ##total population
            sql_str2 = "SELECT population FROM zipcodeData WHERE zipcode='" + zipCode + "' Order by population;"
            try:
                results = self.executeQuery(sql_str2)
                for row in results:
                    self.ui.totalpopList.addItem(str(row[0]))
            except:
                print("totalpop Query failed")

            ##no. of business
            sql_str3 = "SELECT COUNT(business_id) FROM business WHERE zipcode='" + zipCode + "' Order by COUNT(business_id);"
            try:
                results = self.executeQuery(sql_str3)
                for row in results:
                    self.ui.nobusinessList.addItem(str(row[0]))
            except:
                print("no. of business Query failed")

            ##average income
            sql_str4 = "SELECT meanIncome FROM zipcodeData WHERE zipcode='" + zipCode + "' Order by population;"
            try:
                results = self.executeQuery(sql_str4)
                for row in results:
                    self.ui.averageIncomeList.addItem(str(row[0]))
            except:
                print("averageIncomeList Query failed")
            
            ## Business table
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            sql_str = "Select name, address, city, stars, review_count, reviewrating, num_checkins FROM Business WHERE zipcode='" + zipCode + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'No. of Check ins' ])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,230)
                self.ui.businessTable.setColumnWidth(1,230)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,50)
                self.ui.businessTable.setColumnWidth(5,50)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    for colcount in range (0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colcount, QTableWidgetItem(str(row[colcount])))
                    currentRowCount += 1
            except:
                print("zipChanged Query2 failed")

            ## Top category table
            for i in reversed(range(self.ui.topcategoryTable.rowCount())):
                self.ui.topcategoryTable.removeRow(i)

            sql_str6 = "SELECT COUNT(category_name) as nocategory, category_name FROM Business NATURAL JOIN Categories WHERE zipcode='" + zipCode + "' GROUP BY category_name ORDER BY COUNT(category_name) desc;"
            try:
                results = self.executeQuery(sql_str6)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topcategoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.topcategoryTable.setColumnCount(len(results[0]))
                self.ui.topcategoryTable.setRowCount(len(results))
                self.ui.topcategoryTable.setHorizontalHeaderLabels(['# of Business', 'Category'])
                self.ui.topcategoryTable.resizeColumnsToContents()
                self.ui.topcategoryTable.setColumnWidth(0,100)
                self.ui.topcategoryTable.setColumnWidth(1,100)
                currentRowCount = 0
                for row in results:
                    for colcount in range (0,len(results[0])):
                        self.ui.topcategoryTable.setItem(currentRowCount, colcount, QTableWidgetItem(str(row[colcount])))
                    currentRowCount += 1
            except:
                print("zipChanged Query2 failed")

                        ## popular list
            for i in reversed(range(self.ui.popularList.rowCount())):
                self.ui.popularList.removeRow(i)

            sql_str2 = "Select name, num_checkins, reviewrating from Business WHERE zipcode = '" + zipCode + "'  ORDER BY num_checkins desc;"
            try:
                results = self.executeQuery(sql_str2)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularList.horizontalHeader().setStyleSheet(style)
                self.ui.popularList.setColumnCount(len(results[0]))
                self.ui.popularList.setRowCount(len(results))
                self.ui.popularList.setHorizontalHeaderLabels(['Business Name', 'No. of Check ins', 'Review Rating' ])
                self.ui.popularList.resizeColumnsToContents()
                self.ui.popularList.setColumnWidth(0,200)
                self.ui.popularList.setColumnWidth(1,70)
                self.ui.popularList.setColumnWidth(2,170)

                currentRowCount = 0
                for row in results:
                    for colcount in range (0,len(results[0])):
                        self.ui.popularList.setItem(currentRowCount, colcount, QTableWidgetItem(str(row[colcount])))
                    currentRowCount += 1
            except:
                print("popularList Query2 failed")

            ## Successful List
            for i in reversed(range(self.ui.successfulList.rowCount())):
                self.ui.successfulList.removeRow(i)

            sql_str3 = "Select name, num_checkins, reviewrating from Business NATURAL JOIN (SELECT AVG(num_checkins) as avgzipcheckins from Business WHERE zipcode = '" + zipCode + "') WHERE zipcode ='" + zipCode + "'  AND num_checkins > avgzipcheckins ORDER BY reviewrating  desc"
            try:
                results = self.executeQuery(sql_str3)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulList.horizontalHeader().setStyleSheet(style)
                self.ui.successfulList.setColumnCount(len(results[0]))
                self.ui.successfulList.setRowCount(len(results))
                self.ui.successfulList.setHorizontalHeaderLabels(['Business Name', 'No. of Check ins', 'Review Rating' ])
                self.ui.successfulList.resizeColumnsToContents()
                self.ui.successfulList.setColumnWidth(0,200)
                self.ui.successfulList.setColumnWidth(1,70)
                self.ui.successfulList.setColumnWidth(2,170)

                currentRowCount = 0
                for row in results:
                    for colcount in range (0,len(results[0])):
                        self.ui.successfulList.setItem(currentRowCount, colcount, QTableWidgetItem(str(row[colcount])))
                    currentRowCount += 1
            except:
                print("successfulList Query2 failed")

    def categoryChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.CityList.selectedItems()) > 0) and (len(self.ui.ZipCodeList.selectedItems()) > 0) and (len(self.ui.CategoriesList.selectedItems()) > 0):
            zipCode = self.ui.ZipCodeList.selectedItems()[0].text()
            category = self.ui.CategoriesList.selectedItems()[0].text()
            sql_str = "Select name, address, city, stars, review_count, reviewrating, num_checkins FROM Business NATURAL JOIN Categories WHERE zipcode='" + zipCode + "' AND category_name='" + category + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'No. of Check ins' ])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,230)
                self.ui.businessTable.setColumnWidth(1,230)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,50)
                self.ui.businessTable.setColumnWidth(5,50)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    for colcount in range (0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colcount, QTableWidgetItem(str(row[colcount])))
                    currentRowCount += 1
            except:
                print("zipChanged Query2 failed")


    def clearAll(self):
        self.ui.CityList.clear()
        self.ui.ZipCodeList.clear()
        self.ui.CategoriesList.clear()
        self.ui.totalpopList.clear()
        self.ui.nobusinessList.clear()
        self.ui.averageIncomeList.clear()
        self.ui.topcategoryTable.clear()
        self.ui.businessTable.clear()
        self.ui.popularList.clear()
        self.ui.successfulList.clear()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1_project()
    window.show()
    sys.exit(app.exec_())