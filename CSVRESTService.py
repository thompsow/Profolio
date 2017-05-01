#-------------------------------------------------------------------------------
# CSVService - REST API service that takes two CSV files daily.csv and
#              companies.csv and will return the following:
#              1. Merge daily.csv and companies.csv in one data frame using the
#                 id columns.
#              2. The data frame will include daily data from start_date to
#                 end_date (inclusive) for every ID in the request using forward
#                 fill for missing dates.
#              3. It will also have an additional column called difference which
#                 shows the difference between current row's value and "nth" (n)
#                 previous row's value (within a given ID).
#              4. The result frame should be sorted by ID and date.
#-------------------------------------------------------------------------------
# REVISION
# 1.0.0 - WMT Initial release
#-------------------------------------------------------------------------------
from flask import Flask, request
from flask_restful import reqparse, Resource, Api
from CSVCustomerStockTimeSeries import CompanyStockValues

DEBUG = False
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('daily_csv')
parser.add_argument('companies_csv')
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('lag_period')

class StockValuesWithDifferenceTable(Resource):
    def post(self):
        args = parser.parse_args()
        daily_csv = args['daily_csv']
        companies_csv = args['companies_csv']
        start_date = args['start_date']
        end_date = args['end_date']
        lag_period = int(args['lag_period'])
        if DEBUG:
            print "start: %s, end: %s, lag: %d" % (start_date, end_date, lag_period)
        stock_values = CompanyStockValues(daily_csv, companies_csv)
        return {'STOCK_DIFF_CSV': stock_values.GetStockValuesWithDifferenceTable(start_date, end_date, lag_period)}

api.add_resource(StockValuesWithDifferenceTable,
                 '/stock_values_diff_table')

if __name__ == '__main__':
    app.run(debug=DEBUG)
