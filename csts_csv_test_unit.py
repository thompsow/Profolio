# test unit for CSVRESTService
from subprocess import Popen
import requests, atexit, time
import unittest

procs = []
SLEEP = 3 # to wait for REST server to load

def kill_subprocesses():
    for proc in procs:
        proc.kill()

def ManualTest(daily_csv_file_name, companies_csv_file_name,
               start_date, end_date, lag_period, debug=True):
    global procs
    daily_csv = open(daily_csv_file_name,"rb").read()
    if len(companies_csv_file_name):
        companies_csv = open(companies_csv_file_name,"rb").read()
    else:
        companies_csv = ""
    proc = Popen(['c:\\python27\\python.exe','CSVRESTService.py'])
    procs += (proc,)
    time.sleep(SLEEP)
    payload = {'daily_csv':daily_csv, 'companies_csv':companies_csv,
               'start_date':start_date, 'end_date':end_date, 'lag_period':lag_period}
    
    stock_diff_csv = requests.post("http://127.0.0.1:5000/stock_values_diff_table",
                        data = payload).json()['STOCK_DIFF_CSV']
    if debug:
        print stock_diff_csv
    proc.terminate()
    procs.remove(proc)
    return stock_diff_csv

class TestCSVRESTService(unittest.TestCase):        
    def test_case1(self):
        print "\n%s" % ('*'*70)
        print "(POST) payload = {'daily_csv':'daily.csv', 'companies_csv':'', " \
               "'start_date':'1/1/17', 'end_date':'', 'lag_period':2}\n"
        csv = ManualTest("daily.csv", "", "1/1/17", "", 2, False)
        self.assertEqual(len(csv),64)
        print len(csv)
        print csv
        print "%s" % ('*'*70)

    def test_case2(self):
        print "\n%s" % ('*'*70)
        print "(POST) payload = {'daily_csv':'daily.csv', 'companies_csv':'companies.csv', " \
               "'start_date':'1/1/17', 'end_date':'1/7/17', 'lag_period':5}\n"
        csv = ManualTest("daily.csv", "companies.csv", "1/1/17", "1/7/17", 5, False)
        self.assertEqual(len(csv),473)
        print len(csv)
        print csv
        print "%s" % ('*'*70)

    def test_case3(self):
        print "\n%s" % ('*'*70)
        print "(POST) payload = {'daily_csv':'daily.csv', 'companies_csv':'companies.csv', " \
               "'start_date':'1/1/17', 'end_date':'1/20/17', 'lag_period':2}\n"
        csv = ManualTest("daily.csv", "companies.csv", "1/1/17", "1/20/17", 2, False)
        self.assertEqual(len(csv),1716)
        print len(csv)
        print csv
        print "%s" % ('*'*70)

atexit.register(kill_subprocesses)
#ManualTest("daily.csv", "companies.csv", "1/1/17", "1/17/17", 2)
suite = unittest.TestLoader().loadTestsFromTestCase(TestCSVRESTService)
unittest.TextTestRunner(verbosity=2).run(suite)
#======================================================================
