from tkinter import messagebox
import string
import logging
logging.basicConfig(filename = "errors.txt",level=logging.ERROR)

class ManageDbm(object):

    def __init__(self,arg):
        self.arg = arg
        self.dict = open("database.txt",arg)
        

    def __del__(self):
        self.dict.close()


class BankAcct(object):
    account_name = list()
    def __init__(self,pin):
        self.__pin = pin
        self.__acct = ManageDbm("r")
        
        self.__dbm = self.__acct.dict.read().replace("\n","")
        self.DataBase = eval(self.__dbm)
        self.atmCash = self.DataBase[100000][2]

        
        name = BankAcct.account_name[-1]
        for key in self.DataBase:
            if self.__pin in self.DataBase[key] and name in self.DataBase[key]:
                self.AcctNo = key
                self.__name = self.DataBase[key][0]
                self.__bal = int(self.DataBase[key][2])
                break
    
    def CheckPin(self,name):
            
            for key in self.DataBase:
              if (self.__pin in self.DataBase[key] and name in self.DataBase[key]):
                return True
            else: return False
            
    @staticmethod
    def CheckName(name):
        
        database = ManageDbm("r")
        dbm = database.dict.read().replace("\n","")
        DataBase = eval(dbm)
        database.dict.close()
        del database
       
        for key in DataBase:
            if name in DataBase[key]:
                BankAcct.account_name.append(name)
                return True
        else: return False

    @staticmethod
    def ResetPin(name,new):
        
        database = ManageDbm("r")
        db = database.dict.read().replace("\n","")
        del database
        DataBase = eval(db)
       
        for key in DataBase:
            if name in DataBase[key]:
                DataBase[key][1] = new
                break
        else: return False

        db = "{\n"
        for key in DataBase:
            db += str(key)+": "+str(DataBase[key])+",\n"
        db += "}" 

        database = ManageDbm("w")
        try:
            database.dict.write(db)
            del database
            return True
        except BaseException as e:
            logging.error(e)
            del database
            return False
            
            
    def GetBalance(self):
        return self.__bal
    def GetName(self):
        return self.__name
    def GetAccountNo(self):
        return self.AcctNo
    

    def Deposit(self,amnt):
        del self.__acct
        self.__bal += amnt
        return self._Processing()

    def WithDraw(self,amnt):
        if self.__bal-amnt<0:
            messagebox.showwarning("ERROR","Insufficient Funds !!")
            return False
        if self.atmCash - amnt<0:
            msg = "Insufficient Cash In ATM !!\nContact Operator To Deposit More Cash."
            messagebox.showerror("ERROR",msg)
            return False
        
        del self.__acct
        self.atmCash -= amnt
        self.DataBase[100000][2] = self.atmCash
        self.__bal -= amnt
        return self._Processing()

    def DelAcct(self,name):
        for key in self.DataBase:
              if (self.__pin in self.DataBase[key] and name in self.DataBase[key]):
                del self.DataBase[key]
                self.db = "{\n"
                for item in self.DataBase:
                    self.db += str(item)+": "+str(self.DataBase[item])+",\n"
                self.db += "}"
                try:
                    self.__acct = ManageDbm("w")
                    self.__acct.dict.write(self.db)
                except BaseException as e:
                    logging.error(e)
                    messagebox.showerror("ERROR","An Error Occurred,Check Errors.txt To View It")
                    return False
                return True
        else: return False
    
    def _Processing(self):

        self.DataBase[self.AcctNo][2] = self.__bal
        self.db = "{\n"
        for key in self.DataBase:
            self.db += str(key)+": "+str(self.DataBase[key])+",\n"
        self.db += "}"
        
        try:
            self.__acct = ManageDbm("w")
            self.__acct.dict.write(self.db)
        except BaseException as e:
            logging.error(e)
            messagebox.showerror("ERROR","An Error Occurred,Check Errors.txt To View It")            
            return False
        else:
            self.__acct.dict.close()
            return (True,self.__bal)

    def Transfer(self,AcctNo,amnt):
        if self.__bal-amnt<0:
            messagebox.showerror("ERROR","Insufficient Funds !!")
            return False

        for key in self.DataBase:
            if AcctNo == key:
                otherAcctNo = key
                otherName = self.DataBase[key][0]
                otherBal = self.DataBase[key][2]
                break
        else:
            messagebox.showerror("INVALID CREDENTIAL","Recipients's Account Number Is Invalid !!")            
            return False

        del self.__acct
        self.__bal -= amnt
        otherBal += amnt
        self.DataBase[otherAcctNo][2] = otherBal
        self.DataBase[self.AcctNo][2] = self.__bal

        self.db = "{\n"
        for key in self.DataBase:
            self.db += str(key)+": "+str(self.DataBase[key])+",\n"
        self.db += "}" 
        
        try:
            self.__acct = ManageDbm("w")
            self.__acct.dict.write(self.db)
        except BaseException as e:
            logging.error(e)
            messagebox.showerror("ERROR","An Error Occurred,Check Errors.txt To View It")
            return False
        else:
            self.__acct.dict.close()
            return (True,self.__bal)

    def ChangePin(self,new,name):
        del self.__acct
        self.__new = new
        for key in self.DataBase:
              if (self.__pin in self.DataBase[key] and name in self.DataBase[key]):
                self.AcctNo = key
                break
        self.DataBase[self.AcctNo][1] = self.__new
        self.db = "{\n"
        for key in self.DataBase:
            self.db += str(key)+": "+str(self.DataBase[key])+",\n"
        self.db += "}"
        
        try:
            self.__acct = ManageDbm("w")
            self.__acct.dict.write(self.db)
        except BaseException as e:
            logging.error(e)
            messagebox.showerror("ERROR","An Error Occurred,Check Errors.txt To View It")
            return False
        else:
            self.__acct.dict.close()
            return True
        
    def __del__(self):
        del self.__acct

