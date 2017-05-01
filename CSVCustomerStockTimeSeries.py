#-------------------------------------------------------------------------------
# CSVTimeSeries - time series generator class for company stock values
#-------------------------------------------------------------------------------
# REVISION
# 1.0.0 - WMT Initial release
#-------------------------------------------------------------------------------
import pandas as pd
from StringIO import StringIO
from dateutil.parser import parse

#-------------------------------------------------------------------------------
class CompanyStockValues:
    def __init__(self, daily_csv, companies_csv=''):
        self._daily = pd.read_csv(StringIO(daily_csv),parse_dates=[1])
        if len(companies_csv):
            self._companies = pd.read_csv(StringIO(companies_csv))
            self._merged_daily = pd.merge_ordered(
                self._daily, self._companies, fill_method='ffill',left_by='id')
        else:
            self._companies = None
            self._merged_daily = self._daily

    #-------------------------------------------------------------------------------
    def __make_even_time_series(self, uneven, date_range):
        # Note: there may be a more inline method of doing this, but in the interest
        # of time this should surfice to even out the time series with forward fill
        # for each ID group
        groups = uneven.groupby('id')
        series = {}
        for key, group in groups:
            series[key] = \
            pd.merge_ordered(group, date_range, fill_method='ffill',
                             right_by='date').ffill().dropna(axis=0)

        if len(series):
            return pd.concat(series)
        return uneven

    #-------------------------------------------------------------------------------
    def __is_valid_date(self, string):
        try: 
            parse(string)
            return True
        except ValueError:
            return False

    #-------------------------------------------------------------------------------
    def GetStockValuesWithDifferenceTable(self, start_date, end_date='', lag_period=1):
        # check for required start_date value entered
        if type(start_date) in [str,unicode] and self.__is_valid_date(start_date):
            pass
        else:
            print "type: %s" % type(start_date)
            raise ValueError("Incorrect start_date format, should be like MM/DD/YYYY or MM-DD-YYYY")
        
        # make end_date same as start_date if not entered or invalid
        if not self.__is_valid_date(end_date):
            end_date = start_date

        # make a date range frame
        date_range = pd.DataFrame({"date": pd.date_range(start_date, end_date)})

        # do a right merge on the daily stock values frame and the date range frame
        # Note: there might be a more optimal method, but for time, I chose this method
        # the result of the merge will contain only IDs with date values in date range
        uneven = pd.merge_ordered(self._merged_daily, date_range, fill_method='ffill',
                                  right_by='date').ffill().dropna(axis=0)

        # let's forward fill the missing date ranges for each ID
        even = self.__make_even_time_series(uneven, date_range)

        # now let's add a column for current row's value and "nth" (n) previous row's
        # value (within a given ID)
        even['difference'] = \
                           even.groupby('id')['value'].diff(lag_period).fillna(0).astype(int)

        # arrange our columns the order we want them for return
        if 'name' in self._merged_daily.columns:
            even = even[['id','date','name','value','difference']]
        else:
            even = even[['id','date','value','difference']]
            
        # this will be a string in CSV format
        return even.sort_values(by=['id','date']).to_csv(index=False)
