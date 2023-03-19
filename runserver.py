from api import create_app
from api.config import config_dict

app = create_app(config_dict["prod"])

if __name__== '__main__':
    app.run(debug=True, port=8000)