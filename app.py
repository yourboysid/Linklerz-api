from flask import Flask, jsonify, request
from flask_api import status
from sqlalchemy import create_engine
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from multiprocessing.pool import ThreadPool


app = Flask(__name__)

URI = "mysql://uaxtpkcqscrfjxcu:BiC3bxjgJpN12aLbKbwC@byhuxzavekpkpqspeoke-mysql.services.clever-cloud.com:3306/byhuxzavekpkpqspeoke"
e = create_engine(URI, pool_recycle=1800)

app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

oauth = OAuth(app)

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    plan = db.Column(db.String(12), nullable=False)
    confirmation = db.Column(db.String(20), nullable=False)
    linktype = db.Column(db.String(500), nullable=False)
    linkurl = db.Column(db.String(500), nullable=False)
    userid = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    auth = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)



def get_linktype(links):
    finalList = links.split(">")
    return finalList

def sortlinks(list_linkType, list_linkUrl):
    links = []

    for name, url in zip(list_linkType, list_linkUrl):
        link = {"name":name, 'url': url}
        links.append(link)

    return links


@app.route('/')
def index():
    return "<p>Hello world</p>"

@app.get('/api/user/<string:username>')
def getuser(username):

    pool = ThreadPool(processes=2)

    # get userdata from db
    userdata = Users.query.filter_by(username=username).first()

    datatype = request.args.get('type')


    # valid user
    try:

        linkType = userdata.linktype
        linkUrl = userdata.linkurl

        async_task_linkType = pool.apply_async(get_linktype, (linkType,))
        async_task_linkUrl = pool.apply_async(get_linktype, (linkUrl,))

        list_linkType = async_task_linkUrl.get()
        list_linkUrl = async_task_linkType.get() 


        links = sortlinks(list_linkType, list_linkUrl)

    
        if datatype == 'all': 

            phone = userdata.phone
            if phone == '':
                phone = None
            
            finaldata  = {'username':username,'phone': phone, 'email': userdata.email , 'userid': userdata.userid , 'plan': userdata.plan, 'links':len(list_linkType), 'data': links,'status': 'ok'}
        
        elif datatype == 'regular':

            finaldata = {'username':username, 'email': userdata.email  , 'data': links,'status': 'ok'}
        
        else:
            finaldata  = {'username':username,'status': 'type not mentioned','data': 'data not available' }

    # invalid user
    except:
        finaldata  = {'username':username,'status': 'failed','data': 'data not available' }


    return jsonify(finaldata), status.HTTP_201_CREATED


@app.get('/api/users')
def getAllusers():

    # get userdata from db
    allUserdata = Users.query.filter_by().all()


    finalData = []

    id = 1 
    for userData in allUserdata: 
        phone = userData.phone
        if phone == '':
            phone = None
            
        data  = {'id': id ,'username': userData.username,'phone': phone, 'email': userData.email , 'userid': userData.userid , 'plan': userData.plan}

        finalData.append(data)
        id += 1 

    return jsonify(finalData), status.HTTP_201_CREATED


if __name__ == '__main__':
	app.run(debug=True)