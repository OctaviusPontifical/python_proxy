import time

import setting

STATISTIC_WAIT =int(setting.get_param("STATISTIC_WAIT"))
STATISTIC_PATH = (setting.get_param("STATISTIC_PATH"))

class Addres_statistics:
    address_list_temp =[]
    address_list = []

    @classmethod
    def init(self):
        try:
            file = open(STATISTIC_PATH)
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
            time.sleep(STATISTIC_WAIT)
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









