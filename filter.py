import json

black_list_path = "black.list"
transparent_mode = False

class Filter:
    black_list = {}

    @classmethod
    def init(self):
        try:
            file = open(black_list_path)
            self.black_list = json.load(file)
            file.close()
        except FileNotFoundError:
            print("File mot found ")
        except Exception as e:
            print('Не предвиденная ошибка в классе Filter : ', e)
        print("********** Init Filter **********")

    @classmethod
    def filter(self,url,port,path = None):
        if url in self.black_list  :
            if self.black_list[url]['port'] =='all':
                return False
            else:
                for list in self.black_list[url]['port']:
                    if list == port:
                        return False

               # if self.black_list[url]['path'] =='all':
                #    return False
                #else:
                 #   for list in self.black_list[url]['path']:
                  #      if list== path:
                   #         return  False
                    #    elif list == 'all':
                     #       return False
            return True
        else:
            return True
