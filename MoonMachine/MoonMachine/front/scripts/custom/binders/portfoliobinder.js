import fileUploader from "scripts/custom/FileTextUploader";
import tokenSetter from "scripts/custom/RequestForgeryToken";
import jquery from "jquery";
import authenticationOutcome from "scripts/custom/models/AuthenticationOutcome";
import ko from "knockout";
import controlsApi from "scripts/custom/webinterfaces/authorizedcontrolsapi";
import portfolioApi from "scripts/custom/webinterfaces/portfolioapi";
import compilationSocket from "scripts/custom/webinterfaces/compilationapi";
import strategyInfo from "scripts/custom/models/StrategyInfo";
import scriptLimits from "scripts/custom/models/ScriptLimits";

let portfolioApiInstance = new portfolioApi();
let binder = new PortfolioBinder();
ko.applyBindings(new PortfolioBinder());

let fileBox = document.getElementById(binder.FileBoxId());

//script limits
let validationRules;

portfolioApiInstance.GetScriptLimits()
    .then((data) => { validationRules = new scriptLimits(...Object.values(data)); });

function PortfolioBinder()
{
    let self = this;
    self.controlsApi = new controlsApi();
    self.compilationSocket = undefined;

    let publicStuff = {
        ShouldDisplayControl: ko.observable(false),

        BotsStatus: ko.observable(""),
        FileBoxId: ko.observable("authfilebox"),
        LoadingSplashId: ko.observable("loadingpage"),
                
        OnToggle: function()
        {
            if (publicStuff.BotsStatus() !== 'idle')
            {
                answer = window.confirm('Are you sure you want to authenticate the bot while running?');

                if (answer === false)
                {
                    return;
                }
            }
            self.controlsApi
                .ToggleOperations()
                .then(() =>
                {
                    ApplyCurrentStatus();
                })
                .fail(() =>
                {
                    ApplyCurrentStatus();
                });
        },

        OnSubmit: function()
        {
            if (fileBox.files.length === 0) {
                window.alert("no file found for uploading.");
                return;
            }

            ToggleLoadingSplash(true);
            let failPrepend = "failed to upload strategy: ";
            publicStuff.Strategy().language = fileBox.files[0].name.split('.').pop();

            ReinstanceCompilationSocket()
                .then(() => {
                    if (publicStuff.Strategy().id === "") {
                        return portfolioApiInstance.CreateStrategy(publicStuff.Strategy());
                    }

                    else {
                        return portfolioApiInstance.UpdateStrategy(publicStuff.Strategy());
                    }
                })
                .then((strategyId) => {
                    self.fileCompressor.UploadFilesText(self.compilationSocket.Send, true, true);
                })
                .catch((error) => {
                    ToggleLoadingSplash(false);

                    if (error.message !== undefined) {
                        window.alert(failPrepend + error.message);
                    }

                    else if (error.responseText !== undefined) {
                        window.alert(failPrepend + error.responseText);
                    }

                    else {
                        window.alert(failPrepend + error);
                    }
                });
        },
        Strategy: ko.observable(new strategyInfo()),
    };
    self.fileCompressor = new fileUploader(publicStuff.FileBoxId());

    function ToggleLoadingSplash(shouldDisplayBool) {
        switch (shouldDisplayBool) {
            case true:
                jquery("#" + publicStuff.LoadingSplashId()).removeClass("not-loading");
                break;

            case false:
                jquery("#" + publicStuff.LoadingSplashId()).addClass("not-loading");
                break;
        }
    }

    function ReinstanceCompilationSocket()
    {
        return new Promise((resolve, reject) => {
            if (self.compilationSocket !== undefined) {
                self.compilationSocket.Dispose();
            }
            new compilationSocket(OnReceivedMessage)
                .then((instancedWebSocket) => {
                    self.compilationSocket = instancedWebSocket;
                    resolve();
                });
        });
    }

    function ApplyCurrentStatus()
    {
        self.controlsApi
            .GetBotsStatus()
            .then(function(data)
            {
                publicStuff.BotsStatus(data['output']);
            });
    }

    function ApplyShouldDisplayControl() {
        self.controlsApi
            .IsAuthenticated()
            .then((data) => {
                let shouldDisplay = (data['output'] === 'true');
                publicStuff.ShouldDisplayControl(shouldDisplay);
            });
    }

    function OnReceivedMessage(event)
    {
        ToggleLoadingSplash(false);

        if (event.data !== "{}") {
            window.alert(event.data);
        }        
        GetCurrentStrategies()
            .then(ApplyCurrentStrategies);
    }

    function GetCurrentStrategies() {
        return new Promise((resolve, reject) => {
            portfolioApiInstance.GetMyStrategies()
                .then(resolve);
        });
    }

    function ApplyCurrentStrategies(currentStrategies)
    {        
        let unpacked = currentStrategies["output"];

        if (unpacked.length > 0) {
            let datasKeys = Object.keys(unpacked);
            let currentValues = Object.values(unpacked[0]);
            publicStuff.Strategy(new strategyInfo(...currentValues));
        }
    }
    ApplyCurrentStatus();
    ApplyShouldDisplayControl(); 
    GetCurrentStrategies()
        .then(ApplyCurrentStrategies);

    ko.utils.domNodeDisposal.addDisposeCallback(self, () =>
    {
        self.compilationSocket.Dispose();
    });    
    return publicStuff;
}