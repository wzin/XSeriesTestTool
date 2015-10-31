import utilities
import debug
from datetime import datetime
from PyQt4.QtCore import QObject
from PyQt4 import QtSql

class QueryEngine(QObject):
    def __init__(self, filename, parent = None):
        QObject.__init__(self, parent)
        self.context = self._create_context(filename)
        self.create_sql_tables()
    
    def insert(self, direction, packet_type, byte_array):
        loggedtime = str(datetime.now())
        self._insert_changed_packet(direction, packet_type, byte_array, loggedtime)   
        self._insert_received_packet(packet_type, byte_array, loggedtime)
    
    def get_last_packet(self, packet_type):
        sql = """SELECT MAX(ID)
        FROM distinctpackets
        WHERE Class = '%s'
        AND Direction = 'incoming'""" % packet_type
        return self._get_records(sql)
    
    def get_latest_packet(self, packet_type):
        sql = """SELECT *
        FROM distinctpackets
        WHERE Class = '%s'
        AND Direction = 'incoming'
        ORDER BY ID DESC LIMIT 1""" % packet_type
        query = QtSql.QSqlQuery(self.context)
        query.prepare(sql)
        query.exec_()
        if query.next():
            row_id = query.value(0)
            timestamp = query.value(1)
            data = query.value(4)
            return row_id, timestamp, data
        return None, None, None
    
    def create_sql_tables(self):
        query = QtSql.QSqlQuery(self.context)
        sql = """CREATE TABLE IF NOT EXISTS session(
        Timestamp DATETIME,
        PacketID INTEGER NOT NULL)"""
        query.prepare(sql)
        query.exec_()
        sql = """CREATE TABLE IF NOT EXISTS distinctpackets(
        ID INTEGER PRIMARY KEY,
        LastChanged DATETIME,
        Direction TEXT NOT NULL,
        Class TEXT NOT NULL,
        Data TEXT NOT NULL)"""
        query.prepare(sql)
        query.exec_()
        query.finish()
    
    def clear_database(self):
        query = QtSql.QSqlQuery(self.context)
        query.exec_("DELETE FROM session")
        query.exec_("DELETE FROM distinctpackets")
        query.finish()
    
    def _create_context(self, filename):
        context = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        context.setDatabaseName(filename)
        context.open()
        return context
        
    def _has_changed(self, packet_type, byte_array):
        row_id, timestamp, data = self.get_latest_packet(packet_type)
        if row_id is None:
            return True

        sequence = utilities.convert_to_hex_string(byte_array)
        return sequence != data
    
    def _insert_changed_packet(self, direction, packet_type, byte_array, logged_time):
        if not self._has_changed(packet_type, byte_array):
            return
        
        query = QtSql.QSqlQuery(self.context)
        hexstring = utilities.convert_to_hex_string(byte_array)        
        
        query.prepare("INSERT INTO distinctpackets(LastChanged, Direction, Class, Data) VALUES(:date,:direction,:type,:contents)")
        query.bindValue(":date", logged_time)
        query.bindValue(":direction", str(direction))
        query.bindValue(":type", packet_type)
        query.bindValue(":contents", str(hexstring))
        query.exec_()
        query.finish()
        
    def _insert_received_packet(self, packet_type, byte_array, logged_time):
        row_id = self._get_row_id_of_latest_packet(packet_type)
        query = QtSql.QSqlQuery(self.context)
        query.prepare("INSERT INTO session(Timestamp, PacketID) VALUES(:date,:packetid)")
        query.bindValue(":date", logged_time)
        query.bindValue(":packetid", row_id)
        query.exec_()
        query.finish()
                
    def _get_row_id_of_latest_packet(self, packet_type):
        return self.get_last_packet(packet_type)[0]
    
    def _get_records(self, sql):
        query = QtSql.QSqlQuery(self.context)
        if query.isActive():
            debug.Log("Wrapper: previous query is still active")
            return []
        query.prepare(sql)
        if query.exec_():
            list = []
            while query.next():
                list.append(str(query.value(0)))
            debug.Log("Wrapper: %i" % len(list))
            return list
        debug.Log("Wrapper: query did not execute successfully")
        return []
    
    def __del__(self):
        self.context.close()
