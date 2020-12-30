from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

from datetime import datetime
import sys
from os import path
from PyQt5.uic import loadUiType

FORM_x,_=loadUiType(path.join(path.dirname('__file__'),"sales.ui"))
FORM_x1,_=loadUiType(path.join(path.dirname('__file__'),"main.ui"))   
temporary_totalprice=0


import sqlite3

#inventory form
class Another_Main(QMainWindow, FORM_x1):
    def __init__(self,parent=None):
        super(Another_Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        
 
#Button Functions 
    def Handle_Buttons(self):
        pass
    
   
    
#sales window______________________________________________________--------------------------------------------        
class Main(QMainWindow, FORM_x):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.combobox_fill()
        self.get_date()
        self.transactions_id()
        
    def get_date(self):
        today = datetime.now()
        self.date_label.setText(str(today.strftime("%m/%d/%Y")))
        
        
    def transactions_id(self):

        db=sqlite3.connect("countrywingsdatabase.db") #database file
        cursor=db.cursor()
        
        command= ''' SELECT max(transaction_id) from transact''' # db command line filter
        resultDB = cursor.execute(command)
        
        X1=int(resultDB.fetchone()[0]) +1
        
        self.transct_id.setText(str(X1))
#Button Functions 
    def Handle_Buttons(self):
        self.addon_button.clicked.connect(self.add_button)
        self.clear_button.clicked.connect(self.clr_button)
        self.tota_button.clicked.connect(self.totals_button)
        self.accept_button.clicked.connect(self.accept_button_)


    def combobox_fill(self):        
        temporary_totalprice=0
        db=sqlite3.connect("countrywingsdatabase.db") #database file
        cursor=db.cursor()
        
        command= ''' SELECT item_name from inventory''' # db command line filter
        result = cursor.execute(command)
    
        items  = []# list items in inventory
        #loop to insert items to combo box
        for items_inbox in result.fetchall():
            items.append(items_inbox[0])

        for x  in items:
            self.addon_listbox.addItem(x)
    
    
    
    def add_button(self):
        db=sqlite3.connect("countrywingsdatabase.db") #database file
        cursor2=db.cursor()        
        addon_text= str(self.addon_listbox.currentText())         
        getprice= ''' SELECT item_price from inventory where item_name =?''' # db command line filter        
        resultitem_price=cursor2.execute(getprice,[addon_text])        
        item_price=str(resultitem_price.fetchone()[0])        
        addon_list = [ addon_text, item_price ]        
        # addon_list = ['1','12323']
        table = self.addon_table        
        self.addTableRow(table , addon_list) 
        
        global temporary_totalprice
        
        temporary_totalprice=int(temporary_totalprice)+int(item_price)
        
       # print (temporary_totalprice)
        
        
        
    def addTableRow(self, addon_table, addon_list):
        
        row = addon_table.rowCount()
        addon_table.setRowCount(row+1)
        col = 0
        for item in addon_list:
            cell = QTableWidgetItem(str(item))
            addon_table.setItem(row, col, cell)
            col += 1

    def clr_button(self):
        self.addon_table.setRowCount(0)
        global temporary_totalprice
        temporary_totalprice=0
        
        
    def totals_button(self):
        global temporary_totalprice
        
        x=str(self.price_sales_txt.text())
        y=str(self.nbr_clients_txt.text())
        
        z=int(x)*int(y)
        
        total_price1=int(z) +int(temporary_totalprice)
        self.totalprice_label.setText(str(total_price1))
        
        
    def accept_button_(self): #add new transaction
        db=sqlite3.connect("countrywingsdatabase.db") #database file
        cursor=db.cursor()
        
        get_totalprice = int(self.totalprice_label.text())
        get_user = str(self.user_label.text())
        get_date = str(self.date_label.text())
        
        additionrow= (get_totalprice, get_user, get_date)

        
        command= ''' INSERT INTO transact (total_price,user,date) VALUES(?,?,?)''' # db command line filter
        resultDB = cursor.execute(command, additionrow)
        db.commit()
        
        self.transactions_id()

def main():
        app=QApplication(sys.argv)
        window=Main()     
        window.show()
        app.exec_()  
        

def mains():
        app=QApplication(sys.argv)
        window=Another_Main()
        window.show()
        app.exec_() 
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
 #updatelistbox

main()

    
    
    
