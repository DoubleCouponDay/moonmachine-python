import pako from "../node_modules/pako/index";
import jquery from "jquery";
import controlsApi from "./webinterfaces/authorizedcontrolsApi";

export default function FileTextUploader(fileboxNameId)
{
    let self = this;
    self.fileBoxesId = fileboxNameId;
    self.controlsApi = new controlsApi();

    return {
        UploadFilesText: function (requestEngine, compressTextBool, resolvePromiseBool)
        {
            let argumentsAsArray = Array.from(arguments);//fixed bug where arguments was not fully copied. it changes between callbacks!
            argumentsAsArray.splice(0, 3); //only add the extra unknown parameters

            return new Promise((resolve, reject) => {
                let fileBox = document.getElementById(self.fileBoxesId);
                let file = fileBox.files[0];
                let reader = new FileReader();

                reader.onloadend = function SubmitReadersText() 
                {
                    let correctString = reader.result;

                    if (compressTextBool)
                    {
                        CompressText(correctString)
                            .then((compressedText) => {
                                correctString = compressedText;
                                FinallyUpload();
                            });
                    }

                    else {
                        FinallyUpload();
                    }

                    function FinallyUpload() {                        
                        

                        if (resolvePromiseBool) {
                            resolve(requestEngine(correctString, ...argumentsAsArray));
                        }

                        else {
                            requestEngine(correctString, ...argumentsAsArray);
                        }
                    };
                };

                if (file !== null)
                {
                    reader.readAsText(file);
                }

                else
                {
                    window.alert("Input file not found.");
                }
            });
        }
    };

    function CompressText(inputString)
    {
        return new Promise((resolve, reject) =>
        {
            resolve(pako.deflate(inputString));
        })
    }
}

