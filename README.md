# Crop-Doctor API

This API is created to predict disease in a given plant (as per chosen by the user). This API works on FastAPI. Here are some things that need to be made sure of before running the API.

## Things to check -

1. Check if `config.yaml` file exists in the root directory. This file is essential for the working of the models.
2. Check if `models/` folder exists in the root directory. This is the file which contains all the models. Make sure these models exist in the folder -

		models/
			|- Apple.h5
			|- cotton.h5
			|- Grape.h5
			|- Maize.h5
			|- Tomatoleaf.h5
3. Run command `pytest` in the root directory, which will run a series of tests in the file `test_main.py`. The important part is that by the end it should display all tests passed (x passed, 0 failed). Ignore warnings.

## Usage -

To run the API simply use the command: `uvicorn main:app --reload`

## Endpoints -

1. `/plants/` - This endpoint returns list of all endpoints which are used for prediction.
2. Prediction endpoints - 

    An example of this is:
`apple/?str_img={base64 encoded image}` : this will return the predicted class for the given image.

    In total five endpoints for these exist - `apple\`, `cotton\`, `maize\`, `grape\`, `tomato\`