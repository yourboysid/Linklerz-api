from src.main import *

app = Flask(__name__)
CORS(app)

URI = "mysql://uaxtpkcqscrfjxcu:BiC3bxjgJpN12aLbKbwC@byhuxzavekpkpqspeoke-mysql.services.clever-cloud.com:3306/byhuxzavekpkpqspeoke"
e = create_engine(URI, pool_recycle=1800)

app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

oauth = OAuth(app)

db = SQLAlchemy(app)