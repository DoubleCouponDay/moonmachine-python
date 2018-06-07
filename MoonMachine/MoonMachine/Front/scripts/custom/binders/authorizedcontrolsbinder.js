import fileUploader from "custom/FileTextUploader";
import tokenSetter from "custom/RequestForgeryToken";
import jquery from "jquery";
import authenticationOutcome from "custom/models/AuthenticationOutcome";
import ko from "knockout";
import controlsApi from "custom/webinterfaces/authorizedcontrolsapi"; //fixed bug where steal js overrode the default module path

ko.applyBindings(new AuthorizedControlsBinder());

function AuthorizedControlsBinder()
{
    let self = this;
    self.controlsApi = new controlsApi();

    let publicStuff = {
        AuthenticationOutcomes: ko.observableArray([]),

        BotsStatus: ko.observable(""),
        IsSubmitting: ko.observable(false),
        FileBoxId: ko.observable("authfilebox"),

        OnSubmit: function()
        {            
            self.controlsApi
                .GetBotsStatus()
                .then(function(data)
                {
                    if (data['output'] !== 'idle')
                    {
                        answer = window.confirm('Are you sure you want to authenticate the bot while running?');

                        if (answer === false)
                        {
                            return;
                        }
                    }
                    publicStuff.IsSubmitting(true);

                    self.fileUploader
                        .UploadFilesText(self.controlsApi.UploadText, false, true)
                        .then(function onSuccess(returnedData)
                        {
                            publicStuff.IsSubmitting(false); //put at the top so that freezing the window with window.alert() wont leave the loading flag up
                            MapUploadOutputsToObservables(returnedData);
                        })
                        .catch(function onError(message)
                        {
                            publicStuff.IsSubmitting(false);
                            window.alert("authentication failed: " + message);
                        });
                });
        }
    };
    self.fileUploader = new fileUploader(publicStuff.FileBoxId());

    function MapUploadOutputsToObservables(returnedData)
    {
        let frontEndFormatOutcomes = [];
        let returnedKeys = Object.keys(returnedData);

        for (let i = 0; i < returnedKeys.length; i++)
        {
	        let formattedOutcome = (returnedData[returnedKeys[i]] === "") ? true : false;
	        frontEndFormatOutcomes.push(new authenticationOutcome(returnedKeys[i], formattedOutcome));
        }
        publicStuff.AuthenticationOutcomes(frontEndFormatOutcomes);
    }
    return publicStuff;
};