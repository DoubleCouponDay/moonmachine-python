import jquery from "jquery";

export default function PortfolioApi()
{
    let self = this;
    self.baseUrl = "/admin/portfolio/"
    self.languagesUrl = self.baseUrl + "getsupportedlanguages";
    self.getAllUrl = self.baseUrl + "getuserstrategies";
    self.limitsUrl = self.baseUrl + "GetValidationRules";
    self.createStratUrl = self.baseUrl + "createstrategy";
    self.updateStratUrl = self.baseUrl + "putstrategy";

    return {
        GetSupportedLanguages: () =>
        {
            return new Promise(function (resolve, reject)
            {
                jquery.getJSON(self.languagesUrl, resolve)
                    .fail(reject);
            });
        },

        GetMyStrategies: () => {
            return new Promise((resolve, reject) =>
            {
                jquery.getJSON(self.getAllUrl, resolve)
                    .fail(reject);
            });
        },
        GetScriptLimits: () => {
            return new Promise((resolve, reject) => {
                jquery.getJSON(self.limitsUrl, resolve)
                    .fail(reject);
            });
        },
        CreateStrategy: (strategyInfo) => {
            return new Promise((resolve, reject) => {
                jquery.post(self.createStratUrl, strategyInfo, resolve) //for some reason input object gets flatted but input string doesnt
                    .fail(reject);
            });
        },

        UpdateStrategy: (strategyInfo) => {
            return new Promise((resolve, reject) => {
                jquery.post(self.updateStratUrl, strategyInfo, resolve)
                    .fail(reject);
            });
        }
    }
}