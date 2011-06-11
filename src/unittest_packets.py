import unittest
from datablockmodels import *

class TestSDBHandle(unittest.TestCase):
    def setUp(self):
        f = open('sdbmockdata.txt', 'r')
        data = f.readline().split()
        self.sdb1 = sdbMdl()
        self.sdb1.setdata(data)
        data = f.readline().split()
        self.sdb2 = sdbMdl()
        self.sdb2.setdata(data)
        
    def testpacketinfo(self):
        self.assertEquals('SDB', self.sdb1.packetinfo())

    def test_version(self):
        self.assertEquals('1.01', self.sdb1.versionNr())
        self.assertEquals('1.02', self.sdb2.versionNr())

    def test_GMID(self):
        self.assertEquals('123456', self.sdb1.GMID())
        self.assertEquals('563412', self.sdb2.GMID())
        
    def test_status_byte_1(self):
        self.assertEquals(True, self.sdb1.idle())
        self.assertEquals(False, self.sdb1.gameCycle())
        self.assertEquals(True, self.sdb1.powerUp())
        self.assertEquals(False, self.sdb1.reset())
        self.assertEquals(True, self.sdb1.ccceTxComplete())
        self.assertEquals(False, self.sdb2.idle())
        self.assertEquals(True, self.sdb2.gameCycle())
        self.assertEquals(False, self.sdb2.powerUp())
        self.assertEquals(True, self.sdb2.reset())
        self.assertEquals(False, self.sdb2.ccceTxComplete())
        
    def test_status_byte_2(self):
        self.assertEquals(True, self.sdb1.largeWin())
        self.assertEquals(False, self.sdb1.collectCash())
        self.assertEquals(True, self.sdb1.cancelCredit())
        self.assertEquals(False, self.sdb1.progressiveWin())
        self.assertEquals(True, self.sdb1.manufacturerWin0())
        self.assertEquals(False, self.sdb1.manufacturerWin1())
        self.assertEquals(True, self.sdb1.manufacturerWin2())
        self.assertEquals(False, self.sdb2.largeWin())
        self.assertEquals(True, self.sdb2.collectCash())
        self.assertEquals(False, self.sdb2.cancelCredit())
        self.assertEquals(True, self.sdb2.progressiveWin())
        self.assertEquals(False, self.sdb2.manufacturerWin0())
        self.assertEquals(True, self.sdb2.manufacturerWin1())
        self.assertEquals(False, self.sdb2.manufacturerWin2())
        
    def test_status_byte_3(self):
        self.assertEquals(True, self.sdb1.doorOpen())
        self.assertEquals(False, self.sdb1.logicCageOpen())
        self.assertEquals(True, self.sdb1.displayError())
        self.assertEquals(False, self.sdb1.selfAuditError())
        self.assertEquals(True, self.sdb1.memoryError())
        self.assertEquals(False, self.sdb1.cashInputError())
        self.assertEquals(True, self.sdb1.cashOutputError())
        self.assertEquals(False, self.sdb2.doorOpen())
        self.assertEquals(True, self.sdb2.logicCageOpen())
        self.assertEquals(False, self.sdb2.displayError())
        self.assertEquals(True, self.sdb2.selfAuditError())
        self.assertEquals(False, self.sdb2.memoryError())
        self.assertEquals(True, self.sdb2.cashInputError())
        self.assertEquals(False, self.sdb2.cashOutputError())
        
    def test_status_byte_4(self):
        self.assertEquals(True, self.sdb1.auditMode())
        self.assertEquals(False, self.sdb1.testMode())
        self.assertEquals(True, self.sdb1.powerSaveMode())
        self.assertEquals(False, self.sdb1.subsEquipPaySuspended())
        self.assertEquals(True, self.sdb1.mechMeterDisconnected())
        self.assertEquals(False, self.sdb1.manufacturerError0())
        self.assertEquals(True, self.sdb1.manufacturerError1())
        self.assertEquals(False, self.sdb2.auditMode())
        self.assertEquals(True, self.sdb2.testMode())
        self.assertEquals(False, self.sdb2.powerSaveMode())
        self.assertEquals(True, self.sdb2.subsEquipPaySuspended())
        self.assertEquals(False, self.sdb2.mechMeterDisconnected())
        self.assertEquals(True, self.sdb2.manufacturerError0())
        self.assertEquals(False, self.sdb2.manufacturerError1())
        
    def test_status_byte_5(self):
        self.assertEquals(True, self.sdb1.cancelCreditError())
        self.assertEquals(False, self.sdb2.cancelCreditError())
        
    def test_multi_game(self):
        pass
    
    def test_meters(self):
        self.assertEquals('$127.05', self.sdb1.turnover())
        self.assertEquals('$12345678.90', self.sdb1.totalWins())
        self.assertEquals('$2025.40', self.sdb1.cashBox())
        self.assertEquals('$12345678.90', self.sdb1.cancelledCredits())
        self.assertEquals('99999999', self.sdb1.gamesPlayed())
        self.assertEquals('$561.55', self.sdb1.moneyIn())
        self.assertEquals('$22222222.22', self.sdb1.moneyOut())
        self.assertEquals('$12345678.90', self.sdb1.cashIn())
        self.assertEquals('$6040.20', self.sdb1.cashOut())
        self.assertEquals('1111111111', self.sdb1.credits())
        self.assertEquals('????', self.sdb1.miscAccrual())
        self.assertEquals('55555555', self.sdb1.nrpowerUps())
        self.assertEquals('5684', self.sdb1.gamesSinceReboot())
        self.assertEquals('77777777', self.sdb1.gamesSinceDoorOpen())
        self.assertEquals('$0.01', self.sdb1.baseCreditValue())
        self.assertEquals('$12345678.90', self.sdb2.turnover())
        self.assertEquals('$27.24', self.sdb2.totalWins())
        self.assertEquals('$12345678.90', self.sdb2.cashBox())
        self.assertEquals('$785.22', self.sdb2.cancelledCredits())
        self.assertEquals('88888888', self.sdb2.gamesPlayed())
        self.assertEquals('$11111111.11', self.sdb2.moneyIn())
        self.assertEquals('$13.43', self.sdb2.moneyOut())
        self.assertEquals('$2036.40', self.sdb2.cashIn())
        self.assertEquals('$33333333.33', self.sdb2.cashOut())
        self.assertEquals('256382', self.sdb2.credits())
        self.assertEquals('????', self.sdb2.miscAccrual())
        self.assertEquals('174', self.sdb2.nrpowerUps())
        self.assertEquals('66666666', self.sdb2.gamesSinceReboot())
        self.assertEquals('4321', self.sdb2.gamesSinceDoorOpen())
        self.assertEquals('$52.63', self.sdb2.baseCreditValue())
        
    def test_ascii_text(self):
        self.assertEquals('GM001700', self.sdb1.programID1())
        self.assertEquals('', self.sdb1.programID2())
        self.assertEquals('SDM00304', self.sdb1.programID3())
        self.assertEquals('S2X00706', self.sdb1.programID4())
        self.assertEquals('GM001802', self.sdb2.programID1())
        self.assertEquals('ABCD1234', self.sdb2.programID2())
        self.assertEquals('SDM12345', self.sdb2.programID3())
        self.assertEquals('S2X12345', self.sdb2.programID4())
        
    def test_rtp(self):
        self.assertEquals('99.99%', self.sdb1.prtp())
        self.assertEquals('93.96%', self.sdb2.prtp())
        
    def test_secondary_functions(self):
        self.assertEquals(True, self.sdb1.linkedProgSupported())
        self.assertEquals(False, self.sdb2.linkedProgSupported())
        
class TestMDBHandle(unittest.TestCase):
    def setUp(self):
        f = open('mdbmockdata.txt', 'r')
        data = f.readline().split()
        self.mdb1 = mdbMdl()
        self.mdb1.setdata(data)
        data = f.readline().split()
        self.mdb2 = mdbMdl()
        self.mdb2.setdata(data)

    def testmdbstuff(self):
        self.assertEquals('123456', self.mdb1.GMID())
        self.assertEquals('887766', self.mdb2.GMID())
        self.assertEquals('5AA5', self.mdb1.versionNr())
        self.assertEquals('ABCD', self.mdb2.versionNr())
        self.assertEquals('1.05', self.mdb1.mdbType())
        self.assertEquals('1.92', self.mdb2.mdbType())
        
    def testBillAcceptorStatusByte1(self):
        self.assertEquals(False, self.mdb1.stackerDoorOpen())
        self.assertEquals(False, self.mdb1.stackerCommsError())
        self.assertEquals(False, self.mdb1.stackerFailure())
        self.assertEquals(False, self.mdb1.stackerFull())
        self.assertEquals(False, self.mdb1.stackerRemoved())
        self.assertEquals(False, self.mdb1.stackerOutOfService())
        self.assertEquals(True, self.mdb2.stackerDoorOpen())
        self.assertEquals(True, self.mdb2.stackerCommsError())
        self.assertEquals(True, self.mdb2.stackerFailure())
        self.assertEquals(True, self.mdb2.stackerFull())
        self.assertEquals(True, self.mdb2.stackerRemoved())
        self.assertEquals(True, self.mdb2.stackerOutOfService())
        
    def testMiscStatusByte1(self):
        self.assertEquals(True, self.mdb1.cashBoxDropDoorOpen())
        self.assertEquals(True, self.mdb1.printerPaperLow())
        self.assertEquals(True, self.mdb1.validTicketOut())
        self.assertEquals(True, self.mdb1.printerFault())
        self.assertEquals(True, self.mdb1.paperEmpty())
        self.assertEquals(True, self.mdb1.validTicketIn())
        self.assertEquals(False, self.mdb2.cashBoxDropDoorOpen())
        self.assertEquals(False, self.mdb2.printerPaperLow())
        self.assertEquals(False, self.mdb2.validTicketOut())
        self.assertEquals(False, self.mdb2.printerFault())
        self.assertEquals(False, self.mdb2.paperEmpty())
        self.assertEquals(False, self.mdb2.validTicketIn())
        
    def testMiscStatusByte2(self):
        self.assertEquals(False, self.mdb1.ticketInCommsError())
        self.assertEquals(False, self.mdb1.ticketInRejectedByHost())
        self.assertEquals(False, self.mdb1.tenRejects())
        self.assertEquals(False, self.mdb1.miscTicketInError())
        self.assertEquals(False, self.mdb1.ticketLowerThanBCV())
        self.assertEquals(False, self.mdb1.ticketStackingDone())
        self.assertEquals(True, self.mdb2.ticketInCommsError())
        self.assertEquals(True, self.mdb2.ticketInRejectedByHost())
        self.assertEquals(True, self.mdb2.tenRejects())
        self.assertEquals(True, self.mdb2.miscTicketInError())
        self.assertEquals(True, self.mdb2.ticketLowerThanBCV())
        self.assertEquals(True, self.mdb2.ticketStackingDone())
        
    def testNotesMeters(self):
        self.assertEquals('5544332211', self.mdb1.nr5DollarNotes())
        self.assertEquals('1122334455', self.mdb2.nr5DollarNotes())
        self.assertEquals('1122222233', self.mdb1.nr10DollarNotes())
        self.assertEquals('3322222211', self.mdb2.nr10DollarNotes())
        self.assertEquals('4455555566', self.mdb1.nr20DollarNotes())
        self.assertEquals('6655555544', self.mdb2.nr20DollarNotes())
        self.assertEquals('1122222233', self.mdb1.nr50DollarNotes())
        self.assertEquals('3322222211', self.mdb2.nr50DollarNotes())
        self.assertEquals('4455555566', self.mdb1.nr100DollarNotes())
        self.assertEquals('6655555544', self.mdb2.nr100DollarNotes())
        self.assertEquals('1122222233', self.mdb1.ticketsAccepted())
        self.assertEquals('3322222211', self.mdb2.ticketsAccepted())
        self.assertEquals('4455555566', self.mdb1.ticketsRejected())
        self.assertEquals('6655555544', self.mdb2.ticketsRejected())
        self.assertEquals('1122222233', self.mdb1.totBillsAcceptedSpare())
        self.assertEquals('3322222211', self.mdb2.totBillsAcceptedSpare())
        self.assertEquals('$44555555.66', self.mdb1.valBillsAccepted())
        self.assertEquals('$66555555.44', self.mdb2.valBillsAccepted())
        self.assertEquals('112222222233', self.mdb1.totBillsAccepted())
        self.assertEquals('332222222211', self.mdb2.totBillsAccepted())
        self.assertEquals('25111997', self.mdb1.dateTicketPrinted())
        self.assertEquals('14032011', self.mdb2.dateTicketPrinted())
        
if __name__ == '__main__':
    unittest.main()