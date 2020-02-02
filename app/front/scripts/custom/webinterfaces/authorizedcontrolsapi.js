let jquery = require("jquery");

export default function AuthorizedControlsApi()
{
    let self = this;
    self.baseUrl = "/admin/authorizedcontrols/"
    self.toggleUrl = self.baseUrl + "toggleoperations";
    self.statusUrl = self.baseUrl + "getbotsstatus";
    self.uploadUrl = self.baseUrl + "AuthenticateWithFile";
    self.isAuthedUrl = self.baseUrl + "IsAuthenticated";

    return {
        ToggleOperations: () => {
            return new Promise(function (resolve) {
                jquery.post(self.toggleUrl, {}, resolve)
                    .fail(() => {
                        window.alert("failed to toggle the strategy.");
                    });
            });
        },

        GetBotsStatus: () => {
            return new Promise(function (resolve) {
                jquery.getJSON(self.statusUrl, null, resolve)
                    .fail(() => {
                        window.alert("failed to GetBotsStatus.");
                    });
            });
        },

        UploadText: (inputString) => //declared functions are always available at any line in the class.
        {
            return new Promise(function (resolve, reject) {
                jquery.post(self.uploadUrl, { "input": inputString }, resolve)                    
                    .fail(reject);
            });
        },

        IsAuthenticated: () => {
            return new Promise((resolve) => {
                jquery.getJSON(self.isAuthedUrl, resolve)
                    .fail(() => {
                        window.alert("failed to Get IsAuthenticated.");
                    });
            });
        }
    }
}