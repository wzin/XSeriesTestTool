from services import QueryEngine
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4 import QtSql, QtGui

class DataViewManager(QObject):
    def __init__(self, filename, publisher, parent = None):
        QObject.__init__(self, parent)
        self.query_engine = QueryEngine(filename, self)
        self.distinct_table_view_model = ModifiedPacketTableModel(self)
        self.session_table_view_model = AnyPacketTableModel(self)
        self.is_autorefresh_enabled = False
        
        self.connect(publisher, SIGNAL("PACKET_RECEIVED"), self._on_valid_packet_received)

    def _add_record(self, direction, packet):
        self.query_engine.insert(direction, packet)
        if self.is_autorefresh_enabled:
            self.refresh()
    
    def _on_valid_packet_received(self, packet):
        self._add_record("incoming", packet)

    def connect_distinct_data(self, table_view):
        data_model = self.distinct_table_view_model.get_model()
        table_view.setModel(data_model)
    
    def connect_session_data(self, table_view):
        data_model = self.session_table_view_model.get_model()
        table_view.setModel(data_model)
    
    def connect_text_inputs(self, line_edit):
        data_model1 = self.distinct_table_view_model.get_model()
        data_model2 = self.session_table_view_model.get_model()
        line_edit.textChanged.connect(data_model1.setFilterRegExp)
        line_edit.textChanged.connect(data_model2.setFilterRegExp)
        
    def refresh(self):
        self.distinct_table_view_model.refresh_data()
        self.session_table_view_model.refresh_data()

    def setAutoRefresh(self, toggle):
        self.is_autorefresh_enabled = toggle

    def getProxyModel(self):
        return self.distinct_table_view_model.get_model()

    def clearDatabase(self):
        self.query_engine.clear_database()
        self.refresh()

class ModifiedPacketTableModel(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("distinctpackets")
        self.model.sort(0, Qt.DescendingOrder)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(3)
        self.proxy.setDynamicSortFilter(True)
        
    def get_model(self):
        return self.proxy
    
    def refresh_data(self):
        self.model.select()

class AnyPacketTableModel(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable("session")
        self.model.setRelation(1, QtSql.QSqlRelation("distinctpackets", "ID", "Class"))
        self.model.sort(0, Qt.DescendingOrder)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(1)
        self.proxy.setDynamicSortFilter(True)
        
    def get_model(self):
        return self.proxy
        
    def refresh_data(self):
        self.model.select()