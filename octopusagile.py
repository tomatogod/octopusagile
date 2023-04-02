from flask import Flask
import requests
import datetime
import configparser as ConfigParser

def get_period_from():
    getdate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    gethour = str(datetime.datetime.now().strftime("%H"))
    if int(gethour) >= 16:
        period = str(getdate) + "T16:00:00Z"
        return period
    else:
        period = datetime.datetime.today() - datetime.timedelta(days=1)
        period = period.strftime("%Y-%m-%d")
        period = period + "T16:00:00Z"
        return period

def get_period_to():
    getdate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    gethour = str(datetime.datetime.now().strftime("%H"))
    if int(gethour) < 16:
        period = str(getdate) + "T16:00:00Z"
        return period
    else:
        period = datetime.datetime.today() - datetime.timedelta(days=-1)
        period = period.strftime("%Y-%m-%d")
        period = period + "T16:00:00Z"
        return period

app = Flask(__name__)

@app.route('/')
def getlowestrates():
    config = ConfigParser.ConfigParser()
    config.read("./octopusagile.conf")
    apikey = config.get('octopusagile', 'apikey')
    apiurl = config.get('octopusagile', 'apiurl')
    slots = int(config.get('octopusagile', 'slots')) - 1
    getdatefrom = get_period_from()
    getdateto = get_period_to()
    periodfrom = f"?period_from={getdatefrom}"
    periodto = f"&period_to={getdateto}"
    getratesurl = f"{apiurl}{periodfrom}{periodto}"
    headers = {'Authorization': apikey}
    res = requests.get(getratesurl, headers=headers)
    data = res.json()
    value_inc_vat = [x['value_inc_vat'] for x in data['results']]
    prices = sorted(value_inc_vat)
    return str((prices[slots] / 100))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)