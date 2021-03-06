let jquery = require("jquery");
import * as jscookie from "../node_modules/js-cookie/src/js.cookie.js";

Init();

export default function Init() {
    let csrfToken = jscookie.get('csrftoken');

    if (csrfToken === "") {
        window.alert('csrfToken is not present in cookies!');
        return;
    }

    let CsrfSafeMethod = function (method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    //django csrf only works out of the box with html form requests. in order to apply the csrf token to my post requests, I need to alter ajax setup here.
    jquery.ajaxSetup ({
            beforeSend: function (xhr, settings) {
                if (CsrfSafeMethod(settings.type) === false &&
                    this.crossDomain === false) {
                    xhr.setRequestHeader('X-CSRFToken', csrfToken); //fixed bug where string was not in the right format
                }
            }
        });
}