import datetime, csv, sys
import faker
from random import randint
import multiprocess
import time
from typing import *


class DataGen(object):
    """
    A simple wrapper for the faker and random modules that will quickly generate fake data in 5 parallel threads
    and export to a csv. Number of rows should be a multiple of 10.
    """
    def __init__(self: object, filename: str, rownum: int) -> None:
        self.faker = faker.Faker()
        self.__filename__ = filename
        self.rownum = rownum/5
        if self.rownum < int(1000):
            self.chunks = int(self.rownum)
            self.iters = int(1)
        else:
            self.chunks = int(1000)
            self.iters = int(self.rownum/1000)

    def dates(self: object, start: str, end: str) -> None:
        """ To generate dates, provide a start and end date in the form of YYY-MM-DD"""
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d')
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d')        

    def gen(self: object, _queue: Iterable) -> None:
        for i in range(0,self.iters):
            output = []
            for j in range(0,self.chunks):
                obj = {}
                if self.start and self.end:
                    obj["date"] = self.faker.date_between_dates(self.start, self.end)
                obj["campaign_name"] = self.faker.catch_phrase()
                obj["location"] = self.faker.simple_profile()["address"]
                obj["page_name"] = self.faker.uri()
                obj["clicks"] = randint(1,1000)
                obj["impressions"] = randint(1000,100000)
                output.append(obj)
            _queue.put(output)

    def write(self: object, _queue: Iterable, _stop_token: str) -> None:
        self.i = 0
        while True:
            obj = _queue.get()
            if obj == "STOP":
                sys.exit()
            filepath = self.__filename__
            f = open(filepath,'a')
            w = csv.DictWriter(f,obj[0].keys())
            if isinstance(obj,list):
                if self.i == 0:
                    w.writeheader()
                    self.i += 1
            w.writerows(obj)
            f.close()

    def generate(self: object) -> None:
        print("Beginning data generation...")
        start_seconds = time.time()
        queue = multiprocess.Queue()
        w = multiprocess.Process(target=self.write, args=(queue,"STOP"))
        jobs = []
        
        for i in range(0,5):
            p = multiprocess.Process(target=self.gen,args=(queue,))
            jobs.append(p)
            p.start()

        w.start()
        for i, item in enumerate(jobs):
            item.join()
        queue.put("STOP")
        w.join()
        elapsed_time = (time.time() - start_seconds)/60
        print("Generation completed. Elapsed time: ", "{0:.2f}".format(elapsed_time), " minutes")

if __name__ == "__main__":
    dg = DataGen("fakedata_1000.csv",1000)
    dg.dates("2017-01-01","2017-12-31")
    dg.generate()
