from flask import *
import PIL.Image as Image
import os
from api_finger_class import FingerConversion, FingerData


app = Flask(__name__)



@app.route('/', methods=['GET'])
def home_page():
    return 'Welcome to FingerPrint Matcher API'



# Usage: <ip>:7777/scan/?sample=<sample file>&file=<main file>
@app.route('/scan/', methods=['GET'])
def request_page():
    # Retrieve arguments
    sampleFile = request.args.get('sample')
    mainFile = request.args.get('file')

    if (sampleFile == None):
        return "'Sample' argument missing"
    elif  (mainFile == None):
        return "'File' argument missing"
    elif (sampleFile == None and mainFile == None):
        return "Insert valid arguments"


    # Validate existence of arguments
    result = os.path.exists(sampleFile)
    result2 = os.path.exists(mainFile)
    final = str(result) + " " + str(result2)


    # If validation is successful, if extension is not jpg or png convert images to png
    if (result and result2):
        sample_name, sample_ext = os.path.splitext(sampleFile)
        main_name, main_ext = os.path.splitext(mainFile)

        if (sample_ext == ".jpg" or sample_ext == ".png"):
            finalSample = sampleFile
        else:
            finalSample = FingerConversion(sampleFile).sample_conversion()

        if (main_ext == ".jpg" or main_ext == ".png"):
            finalMain = mainFile
        else:
            finalMain = FingerConversion(mainFile).sample_conversion()

        
         # Matching Algorithm
        scan = FingerData(finalSample, finalMain)
        final = scan.match()
        scan.clean()


    else:
        # One or both files do not exist
        if (not result):
            return "Sample file not found"
        elif  (not result2):
            return "Main file not found"
        elif (not result and not result2):
            return "Sample file and Main file not found"


    return final






if __name__ == '__main__':
    app.run(port=7777)
