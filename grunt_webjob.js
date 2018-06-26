var stealTools = require("steal-tools"); //using the nodejs import format

module.exports = function(grunt) //using the nodejs module format
{	
	grunt.initConfig({
		pkg: grunt.file.readJSON('../../package.json'),
		
	});
	
	grunt.loadNpmTasks('grunt-browserify');
	
}