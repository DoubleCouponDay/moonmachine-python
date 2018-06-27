module.exports = function(grunt) //using the nodejs module format
{	
	let configobject = {
		pkg: grunt.file.readJSON('package.json'),

		browserify: { //incorporating browserify breaking changes ugh
			development: {
				files: {

				},

				browserifyOptions: {
					debug: true,
				}
			},
			// production: {
			// 	src: [],
			// 	dest: "",
			// 	browserifyOptions: {
			// 		debug: true,
			// 	}
			// }
		},
		
		babel: {
			options: {
				
			},
			
			target: {							
				files: {
					
				}
			}
		}
	};
	configobject = SetBundlePaths(configobject);
	grunt.initConfig(configobject);		
	
	require('load-grunt-tasks')(grunt);
	grunt.registerTask("development", ["babel"]);
	grunt.registerTask("production", ["babel"]);
}

function SetBundlePaths(configobject)
{ //file objects format
	let authbinderpath = "app/static/scripts/custom/binders/authorizedcontrolsbinder.js";
	let portbinderpath = "app/static/scripts/custom/binders/portfoliobinder.js";	
	
	configobject.browserify.development.files[authbinderpath] = [authbinderpath];
	configobject.browserify.development.files[portbinderpath] = [portbinderpath];
	
	configobject.babel.target.files[authbinderpath] = [authbinderpath];
	configobject.babel.target.files[portbinderpath] = [portbinderpath];
	return configobject;
}

