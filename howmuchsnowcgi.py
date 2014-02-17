#!/usr/bin/env python2.7
import sys
sys.path.append('/home/mmachenry/HowMuchSnow')
from flask import Flask, request
from flup.server.fcgi import WSGIServer
import howmuchsnow
import pages
import sqlalchemy as sa

app = Flask(__name__)

engine = sa.create_engine(howmuchsnow.DB)
conn = engine.connect()

@app.route("/")
def index():
    ip_addr = request.environ['REMOTE_ADDR']
    inches = howmuchsnow.how_much_snow_ipv4(ip_addr, conn)
    amount = format_amount(inches)
    homepage = pages.make_homepage(amount)
    return homepage

@app.route("/faq")
def faqpage():
    return pages.faq

def unit_word (inches):
    if inches == 1:
        return "inch"
    else:
        return "inches"

def format_amount(inches):
    reported_value = int(round(inches))
    unit = unit_word(reported_value)
    return str(reported_value) + ' ' + unit

if __name__ == '__main__':
    WSGIServer(app).run()
