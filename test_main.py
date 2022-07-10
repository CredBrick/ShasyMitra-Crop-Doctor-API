from fastapi.testclient import TestClient
from main import CONFIG_FILE, app
import base64
import yaml

client = TestClient(app)

# testing config
CONFIG_FILE = './config.yaml'

def test_config():
    stream = open(CONFIG_FILE, 'r')
    config = yaml.safe_load(stream)

    assert config['PLANTS'] == ['apple', 'cotton', 'grape', 'maize', 'tomato']
    assert config['APPLE']['MODEL'] == 'Apple.h5'
    assert config['COTTON']['MODEL'] == 'cotton.h5'
    assert config['GRAPE']['MODEL'] == 'Grape.h5'
    assert config['MAIZE']['MODEL'] == 'Maize.h5'
    assert config['TOMATO']['MODEL'] == 'Tomatoleaf.h5'

# Open and encode images to test
img = open('./tests/test_img.jpg','rb')
str_img = base64.b64encode(img.read()+b'==').decode('utf-8')

img2 = open('./tests/test_img2.jpg','rb')
str_img2 = base64.b64encode(img2.read()+b'==').decode('utf-8')

# Defining tests for endpoints
def test_apple_disease():
    response = client.get(f'/apple/?str_img={str_img}')
    assert response.status_code==200

def test_cotton_disease():
    response = client.get(f'/cotton/?str_img={str_img2}')
    assert response.status_code==200

def test_grape_disease():
    response = client.get(f'/grape/?str_img={str_img}')
    assert response.status_code==200

def test_maize_disease():
    response = client.get(f'/maize/?str_img={str_img2}')
    assert response.status_code==200

def test_tomato_disease():
    response = client.get(f'/tomato/?str_img={str_img}')
    assert response.status_code==200