import threading
import time

time_weit_statistic_analis =10 # in sec

class Addres_statistics:
    address_list_temp =[]
    address_list = []

    @classmethod
    def init(self):
        try:
            file = open('address')
            for line in file:
                addr=  line.rstrip('\n')
                self.address_list.append(addr)
            file.close()
        except FileNotFoundError:
            print("File mot found ")
        except Exception as e:
            print('Не предвиденная ошибка :', e)
        print("********** Init Statistic **********")

    @classmethod
    def addres_statistic_loop(self):
        while True:
            time.sleep(time_weit_statistic_analis)
            file = open("address", 'a')
            temp_list = set(self.address_list_temp)
            self.address_list_temp = []
            for i in temp_list:
                try:
                    self.address_list.index(i)
                except ValueError :
                    self.address_list.append(i)
                    file.write(i+"\n")
            file.close()









