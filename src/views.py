from src.main import *

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

@app.route('/api/<string:username>', methods = ['GET'])
def getuser(username):


    # get userdata from db
    userdata = Users.query.filter_by(username=username).first()

    datatype = request.args.get('type')


    # valid user
    try:

        linkType = userdata.linktype
        linkUrl = userdata.linkurl

        list_linkType = get_linktype(linkType)
        list_linkUrl = get_linktype(linkUrl)

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