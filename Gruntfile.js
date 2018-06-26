var stealTools = require("steal-tools"); //using the nodejs import format

module.exports = function(grunt) //using the nodejs module format
{	
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		"steal-build": {
			default: {
			  options: {
				steal: {
				  config: __dirname + "/MoonMachine/MoonMachine/static/scripts/package.json!npm",
				  main: "scripts/custom/binders/mainbinder"
				},
				buildOptions: {
				  minify: true,
				  sourceMaps: false
				}
			  }
			}
		  }
	});
	
	grunt.loadNpmTasks("grunt-steal");
	grunt.registerTask("default", "steal-build");
}