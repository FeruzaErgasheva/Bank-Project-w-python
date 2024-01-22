from datetime import datetime
import csv
class InputError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class InsufficeintMOney(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Bank:
    all=[]
    def __init__(self,name,comission:float,virtualMoney:float,cash:float) -> None:
        self.name=name
        self.__comission=comission
        self.__virtualMoney=virtualMoney
        self.__cash=cash
        
        Bank.all.append(self)
    @property
    def cash(self):
        return self.__cash
    @property
    def virtualMoney(self):
        return self.__virtualMoney
    @property
    def comission(self):
        return self.__comission
    @classmethod
    def csv_banks(cls):
        with open("bank/bank.csv","r") as fbanks:
            reader=csv.DictReader(fbanks)
            banks=list(reader)
            for bank in banks:
                Bank(
                    name=bank.get('name'),
                    comission=float(bank.get("comission")),
                    virtualMoney=float(bank.get('virtualMoney')),
                    cash=float(bank.get('cash'))
                )
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name},{self.__comission},{self.__virtualMoney},{self.__cash})"
    def cashUpdate(self,moneyAmount:float):
        self.__cash+=moneyAmount
    def virtualMoneyUpdate(self,moneyAmount):
        self.__virtualMoney+=moneyAmount
       
    

class BankAccount:
    def __init__(self,name,id,password,phnumber:str,balance:0,paymentHistory=[]) -> None:
        self.__name=name
        self.__id=id
        self._password=password
        self.__phnumber=phnumber
        self.__balance=balance
        self.__paymentHistory=[]
        
    def getAccountInfo(self):
        return f"""
    name:{self.__name}
    id:{self.__id}
    phnumber={self.__phnumber}
    balance={self.__balance}
    """
    
    def getId(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    @property
    def phnumber(self):
        return self.__phnumber
    @property
    def getBalance(self):
        return self.__balance
    def getPaymentHistory(self):
        return self.__paymentHistory    
    def recordPayment(self,time:str,counterpart:str,money:str,updatedBalance):
        paymentInfo={
            "Card owner name":self.__name,
            "time":time,
            "Agreement made with":counterpart,
            "money":money,
            "Current balance":updatedBalance
        }
        self.__paymentHistory.append(paymentInfo)
    
    @name.setter
    def nameSetter(self,newName):
        if isinstance(newName,str):
            self.__name=newName
        else:
            raise InputError
        
    @phnumber.setter
    def phnumberSetter(self,newNumber:str):
        if newNumber.startswith("99899")  or newNumber.startswith("99897") or newNumber.startswith("99890"):
            self.__phnumber=newNumber
        else:
            raise InputError
        
    def addBalance(self,amount:float,index):
        totalMoney=amount+amount * Bank.all[index].comission
        if amount>0 and Bank.all[index].virtualMoney>=totalMoney:
            self.__balance+=amount
            currentTime=datetime.now().strftime("%H:%M:%S")
            counterpart=Bank.all[index].name
            self.recordPayment(currentTime,counterpart,str(f"+{amount}"),self.__balance)
            Bank.all[index].cashUpdate(totalMoney)
            Bank.all[index].virtualMoneyUpdate(-amount)   
        elif Bank.all[index].virtualMoney<amount:
            raise InsufficeintMOney("bankda pul yetarli emas")
        
        
    #paymenthistory
    def withdraw(self,money,index):
        totalMoney=money+money*Bank.all[index].comission
        if self.__balance-totalMoney<0:
            raise  InsufficeintMOney("Kartezda buncha puliz yo'q")
        elif money<0:
            raise InputError("Pul manfy qiymat bo'la olmaydi")
        else:
            self.__balance-=totalMoney
            counterpart=Bank.all[index].name
            currentTime=datetime.now().strftime("%H:%M:%S")
            self.recordPayment(currentTime,counterpart,str(f"-{money}"),self.__balance)
            Bank.all[index].cashUpdate(-money)
            Bank.all[index].virtualMoneyUpdate(totalMoney)
            
    
    def transfer(self,toAccount:object,transferMoney:float,bankCardIndex:int):
        comission=Bank.all[bankCardIndex].comission
        totalMoney=(transferMoney+transferMoney*comission)
        if self.__balance-totalMoney>=0:
            self.__balance-=totalMoney
            toAccount.__balance+=transferMoney
            currentTime=datetime.now().strftime("%H:%M:%S")
            self.recordPayment(currentTime,toAccount.__name,str(f"-{totalMoney}"),self.__balance)
            toAccount.recordPayment(currentTime,self.__name,str(f"+{transferMoney}"),toAccount.__balance)
        else:
            raise InsufficeintMOney
        
        

Bank.csv_banks()
user1=BankAccount("Feruza","03015","20060406","998993030917",200_000,[])
user2=BankAccount("Fayoza","03255","11042004","998908191104",0,[])
# user1.addBalance(200_000,0)
# print(user1.getPaymentHistory())
# print(Bank.all[0].cash)
# print(Bank.all[0].virtualMoney)
# user1.withdraw(150000,0)
# print(user1.getPaymentHistory())
user1.transfer(user2,50000,0)
print(user1.getPaymentHistory())
print(user2.getPaymentHistory())
user2.addBalance(120000,1)
print(user2.getPaymentHistory())
user2.transfer(user1,60000,0)
print(user1.getPaymentHistory())
print(user2.getPaymentHistory())

            

        
    
   
        
       