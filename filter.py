import time

import setting

BLACK_LIST_PATH = setting.get_param("BLACK_LIST_PATH")
BLACK_LIST_WAIT = int(setting.get_param("BLACK_LIST_WAIT"))
transparent_mode = False

class Filter:
    black_list = {}

    @classmethod
    def init(self):
        try:
            file = open(BLACK_LIST_PATH)
            for line in file:
                site,domain,port,subdomain,source=line.rstrip('\n').split(":")
                self.black_list[site]={}
                self.black_list[site]["domain"]=domain
                self.black_list[site]["port"]=port
                self.black_list[site]["subdomain"]=subdomain
                self.black_list[site]["source"]=source
            file.close()
        except FileNotFoundError:
            print("File mot found ")
        except Exception as e:
            print('Не предвиденная ошибка в классе Filter : ', e)
        print("********** Init Filter **********")

    @classmethod
    def filter(self,url,port,source=None):
        site = url.split(".")
        if site[-2] in self.black_list  :
            if self.black_list[site[-2]]['domain'] == '': None
            elif self.black_list[site[-2]]['domain'] == 'all': return False
            else:
                if site[-1] in self.black_list[site[-2]]['domain'].split(","):
                    return False

            if self.black_list[site[-2]]['port'] =='': None
            elif self.black_list[site[-2]]['port'] == 'all' : return False
            else:
                if port in self.black_list[site[-2]]['port'].split(","):
                    return False

            if len(site) >2:
                if self.black_list[site[-2]]['subdomain'] =='': None
                elif self.black_list[site[-2]]['subdomain'] == 'all' : return False
                else:
                    if site[-3] in self.black_list[site[-2]]['subdomain'].split(","):
                        return False

            if self.black_list[site[-2]]['source'] =='': None
            elif self.black_list[site[-2]]['source'] == 'all' : return False
            else:
                if source in self.black_list[site[-2]]['source'].split(","):
                    return False

            return True

        elif url in self.black_list:
            if self.black_list[url]['port'] =='': None
            elif self.black_list[url]['port'] == 'all' : return False
            else:
                if port in self.black_list[url]['port'].split(","):
                    return False

            if self.black_list[url]['source'] =='': None
            elif self.black_list[url]['source'] == 'all' : return False
            else:
                if source in self.black_list[url]['source'].split(","):
                    return False

            return True
        else:
            return True

    @classmethod
    def update_blacklist_loop(self):
        while True:
            time.sleep(BLACK_LIST_WAIT)
            temp = {}
            try :
                file = open(BLACK_LIST_PATH)
                for line in file:
                    site,domain,port,subdomain,source=line.rstrip('\n').split(":")
                    temp[site]={}
                    temp[site]["domain"]=domain
                    temp[site]["port"]=port
                    temp[site]["subdomain"]=subdomain
                    temp[site]["source"]=source
                file.close()
                self.black_list = temp
            except FileNotFoundError:
                print("Black list mot found ")
            except Exception as e:
                print('Не предвиденная ошибка в классе Filter : ', e)