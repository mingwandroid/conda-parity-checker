import threading
import time
import os
from flask import Flask
from flask import render_template
from datetime import datetime
from utils import compare_versions, r_con, update_info

app = Flask(__name__)

@app.route('/')
def homepage():

     pkg_info = {}
     status_order = {'🤔🤔🤔': 1, '🤔🤔': 2, '🤔': 3, '✓': 4, '🎉': 5}
     for channel in ['conda-forge', 'anaconda', 'c3i_test']:
         res = r_con.hgetall(channel)
         res = {k.decode(): (v.decode().split('#')[0], v.decode().split('#')[1])
                 for k, v in res.items()}
         pkg_info[channel] = []
         for k, v in res.items():
             pkg_info[channel].append({'pkg_name': k,
                 'pkg_status': compare_versions(v[0], v[1]),
                 'pkg_ver': v[0],
                 'pip_ver': v[1]})
         pkg_info[channel].sort(key = lambda x: status_order[x['pkg_status']])

     return render_template("index.html", pkg_info=pkg_info)


def infinity():
    while True:
        try:
            update_info(['conda-forge', 'anaconda', 'c3i_test'])
        except:
            pass
        time.sleep(3600)

if __name__ == '__main__':
    print('first thread')
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': int(os.environ.get('PORT', 5000))}).start()
    print('second thread')
    threading.Thread(target=infinity).start()
