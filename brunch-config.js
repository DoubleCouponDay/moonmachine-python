// See http://brunch.io for documentation.
exports.files = {
	javascripts: {
		entryPoints: {

		}

	},
	stylesheets: {
		joinTo: 'stylesheets/app.css'
	},
	templates: {
		joinTo: 'javascripts/app.js'
	}
	conventions: {
		ignored: "/app/front"
	},
	paths: {
		public: "/app/static",
		watched: ["app"]
	}
};

let authbinderpath = "app/static/scripts/custom/binders/portfoliobinder.js";
let portbinderpath = "app/static/scripts/custom/binders/portfoliobinder.js";

exports.files["javascripts"]["entryPoints"][authbinderpath] = authbinderpath;
exports.files["javascripts"]["entryPoints"][portbinderpath] = portbinderpath;



