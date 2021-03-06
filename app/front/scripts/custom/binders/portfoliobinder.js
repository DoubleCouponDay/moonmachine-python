let jquery = require("jquery");
let ko = require("knockout");
import fileUploader from "../FileTextUploader.js";
import "../RequestForgeryToken.js";
import controlsApi from "../webinterfaces/authorizedcontrolsapi.js";
import portfolioApi from "../webinterfaces/portfolioapi.js";
import compilationSocket from "../webinterfaces/compilationapi.js";
import strategyInfo from "../models/StrategyInfo.js";

let portfolioApiInstance = portfolioApi();
let binder = PortfolioBinder();
ko.applyBindings(PortfolioBinder());

let fileBox = document.getElementById(binder.FileBoxId());

function PortfolioBinder()
{
    let self = this;
    self.controlsApi = controlsApi();
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
                let answer = window.confirm('Are you sure you want to authenticate the bot while running?');

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
                .then(() => {
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
        Strategy: ko.observable(strategyInfo()),
    };
    self.fileCompressor = fileUploader(publicStuff.FileBoxId());

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
        return new Promise((resolve) => {
            if (self.compilationSocket !== undefined) {
                self.compilationSocket.Dispose();
            }
            compilationSocket(OnReceivedMessage)
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
        return new Promise((resolve) => {
            portfolioApiInstance.GetCreatedStrategies()
                .then(resolve);
        });
    }

    function ApplyCurrentStrategies(currentStrategies)
    {        
        let unpacked = currentStrategies["output"];

        if (unpacked.length > 0) {
            let currentValues = Object.values(unpacked[0]);
            publicStuff.Strategy(strategyInfo(...currentValues));
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