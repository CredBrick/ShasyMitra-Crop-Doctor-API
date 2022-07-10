from fastapi import FastAPI, Request
import yaml
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from fastapi.responses import HTMLResponse
from base_model.model import MLModel

# Initialise FAST-API
app = FastAPI()

# Load configs
CONFIG_FILE = './config.yaml'
config = {}

try:
    stream = open(CONFIG_FILE, 'r')
    config = yaml.safe_load(stream)

except:
    print('Config file not found!')
    exit()

# Load all the models as global variables
MODEL_PATH = './models'

try:
    APPLE_MODEL = MLModel(os.path.join(MODEL_PATH, config['APPLE']['MODEL']),config['APPLE']['OUTPUT_CLASSES'])
    COTTON_MODEL = MLModel(os.path.join(MODEL_PATH, config['COTTON']['MODEL']),config['COTTON']['OUTPUT_CLASSES'])
    GRAPE_MODEL = MLModel(os.path.join(MODEL_PATH, config['GRAPE']['MODEL']),config['GRAPE']['OUTPUT_CLASSES'])
    MAIZE_MODEL = MLModel(os.path.join(MODEL_PATH, config['MAIZE']['MODEL']),config['MAIZE']['OUTPUT_CLASSES'])
    TOMATO_MODEL = MLModel(os.path.join(MODEL_PATH, config['TOMATO']['MODEL']),config['TOMATO']['OUTPUT_CLASSES'])

except Exception as e:
    print('Model files not found!\n Exception recorded:',e)
    exit()

# Defining a generic function to take model as input and return prediction
def model_pipeline(model, model_name, str_img):
    """function containing entire model pipeline

    Args:
        model (tf model): tf model
        model_name (str): model name as given in config file
        str_img (str): base64 encoded image as a string

    Returns:
        str: predicted class for a given image
    """
    image = model.decode_image(str_img)
    image = model.preprocess(
        image, 
        tuple(config[model_name]['INPUT_SIZE']), 
        normalize = config[model_name]['NORMALIZE']
    )
    return model.predict(image)

# Root path documentation as a guide
@app.get("/")
def index(request: Request):
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Crop-Doctor API</h1>"
        "<div>"
        "<p> This API hosts the following endpoints - </p>"
        "<ol>"
        "<li> <b>/plants</b> - returns list of all endpoints (for prediction) </li>"
        "<li> <b>/apple</b> - queries a base64 encoded image and returns a predicted class"
        "<li> <b>/grape</b> - queries a base64 encoded image and returns a predicted class"
        "<li> <b>/maize</b> - queries a base64 encoded image and returns a predicted class"
        "<li> <b>/cotton</b> - queries a base64 encoded image and returns a predicted class"
        "<li> <b>/tomato</b> - queries a base64 encoded image and returns a predicted class"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

# Define endpoints for each model
@app.get("/apple/")
async def apple_disease(str_img: str=""):
    return {"result" : model_pipeline(APPLE_MODEL, 'APPLE', str_img)}

@app.get("/cotton/")
async def cotton_disease(str_img: str=""):
    return {"result" : model_pipeline(COTTON_MODEL, 'COTTON', str_img)}

@app.get("/grape/")
async def grape_disease(str_img: str=""):
    return {"result" : model_pipeline(GRAPE_MODEL, 'GRAPE', str_img)}

@app.get("/maize/")
async def maize_disease(str_img: str=""):
    return {"result" : model_pipeline(MAIZE_MODEL, 'MAIZE', str_img)}

@app.get("/tomato/")
async def tomato_disease(str_img: str=""):
    return {"result" : model_pipeline(TOMATO_MODEL, 'TOMATO', str_img)}

# Define one final endpoint which will return list of endpoints
@app.get("/plants")
async def plants():
    return {"plants":config['PLANTS']}