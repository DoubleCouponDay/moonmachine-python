import fileUploader from "../FileTextUploader";
import tokenSetter from "../RequestForgeryToken";
import jquery from "jquery";
import authenticationOutcome from "../models/AuthenticationOutcome";
import ko from "knockout";
import controlsApi from "../webinterfaces/authorizedcontrolsApi";
import portfolioApi from "../webinterfaces/portfolioapi";
import compilationSocket from "../webinterfaces/compilationapi";
import strategyInfo from "../models/StrategyInfo";
import scriptLimits from "../models/ScriptLimits";

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
        Loading: ko.observable(false),
        FileBoxId: ko.observable("authfilebox"),
                
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

            publicStuff.Loading(true);
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
        publicStuff.Loading(false);
        window.alert("compilation: " + event.data);
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