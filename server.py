import pyrebase
from openalpr import Alpr
from time import gmtime, strftime
import sys

# firebase vars +
accuracy = 0
lpn = ''
write_data = {}
url = 'https://lpr-emkay.firebaseio.com/'
child = 'cars'

config = {
    "apiKey": "AIzaSyC4YfdwKN7s4ZUZRcDuDcHH388x67TXpa4",
    "authDomain": "lpr-emkay.firebaseapp.com",
    "databaseURL": url,
    "projectId": "lpr-emkay",
    "storageBucket": "lpr-emkay.appspot.com",
    "serviceAccount" : "./conf/lpr-emkay-firebase-adminsdk-kfim8-7f672d2961.json"
}

# openalpr vars
region = 'eu'
topn = 2

# TODO replace with image link ip camera
# TODO replace with raspberry pi image
plate_link = "nine.jpg"

class ManFirebase():
    global url, write_data, accuracy, lpn, region, topn, plate_link, config, child

    def __init__(self):
        self.config = config
        self.child = child

        ####
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()

        self.write_data = write_data
        self.accuracy = accuracy
        self.lpn = lpn
        self.post_date = strftime("%a, %d %b %Y %H:%M:%S", gmtime())

        self.region = region
        self.topn = topn
        self.plate_link = plate_link
        self.start = 0
        self.alpr = Alpr(self.region, './conf/def_one.defaults', './openalpr/runtime_data')
        self.alpr.set_top_n(self.topn)
        self.alpr.set_default_region('md')
    
    def get_data(self):
        self.data = self.db.child(self.child).get()
        print(self.data)

    def write(self):
        new_car = {'accuracy': self.accuracy, 'date': self.post_date, 'lpn': self.lpn }
        self.db.child(self.child).push(new_car)
        print(new_car)

    def recognize_plates(self):
        self.plate_result = self.alpr.recognize_file(self.plate_link)
        for plate_number in self.plate_result['results']:
            self.start += 1
            for candiate in plate_number['candidates']:
                self.lpn = candiate['plate']

                self.accuracy = candiate['confidence']
        
        self.alpr.unload()
        if self.lpn == '':
            print("No plates recognozed")
            sys.exit(1)

        self.write()

transact = ManFirebase()
def recognize():
    transact.recognize_plates()
    #transact.get_data()
if __name__ == "__main__":
    #print plate_link
    recognize()