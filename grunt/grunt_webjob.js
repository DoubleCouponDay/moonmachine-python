let parcel = require("parcel");
let async = require("async");
let path = require("path");
let filesystem = require("fs");
let javascriptfolder = "../app/static/scripts/";
let filestobundle = "../app/static/scripts/custom/binders";

module.exports = function(grunt) //using the nodejs module format
{	
	let configobject = {
		pkg: grunt.file.readJSON('package.json'),

		browserify: { //incorporating browserify breaking changes ugh
			development: {
				files: [],

				options: {
					debug: true
				}
			},
			production: {
				files: [],
				
				options: {
				
				}
			}
		},
		
		babel: {
			production: {
				files: []
			}
		}
	};
	configobject = SetPaths(configobject);
	grunt.initConfig(configobject);		
	
	require('load-grunt-tasks')(grunt);
	
	grunt.registerTask("parcel", "description", parceltask);
	
	grunt.registerTask("development", ["parcel:true"]);
	grunt.registerTask("production", ["babel:production", "parcel:false"]);
};

function SetPaths(configobject)
{
	let alljsfiles = { //dynamic file mappings
		expand: true,
		cwd: javascriptfolder,
		src: ["**/*.js"],
		dest: javascriptfolder	
	};
	configobject.babel.production.files = [alljsfiles];
	return configobject;
}

function parceltask(debugmodebool) 
{	
	let done = this.async(); //grunt specific command for making an asynchronous task.		
	let directory = path.join(__dirname, filestobundle);	

	let parceloptions = {
		outDir: directory,
		cache: false,
		logLevel: 3,
		minify: debugmodebool === false,
		sourceMaps: true
	};	
	deletepreviousbundles(directory);
	renamebundlestomin(directory);
	buildbundles(parceloptions, directory, done);
}

function deletepreviousbundles(directory)
{
	let files = filesystem.readdirSync(directory);
	
	for (let i = 0; i < files.length; i++)
	{
		let removefilecomponents = files[i].split(".");

		if (removefilecomponents[1] === "min")
		{			
			let absolutelocation = path.join(directory, files[i]); //fixed bug where parcel could not find file
			console.log("deleting previous bundle: " + absolutelocation);
			filesystem.unlinkSync(absolutelocation);
		}
	}
}

function renamebundlestomin(directory)
{
	console.log("renaming bundle inputs so that source maps may work.");
	let files = filesystem.readdirSync(directory);

	for (let i = 0; i < files.length; i++)
	{
		console.log("renaming " + files[i]);
		let filenamecomponents = files[i].split(".");
		let newpath = directory + "/" + filenamecomponents[0] + ".min.js";
		let oldpath = path.join(directory, files[i]);

		console.log("renameoldpath: " + oldpath);
		console.log("renamenewpath: " + newpath);
		filesystem.renameSync(oldpath, newpath);
	}
}

function buildbundles(parceloptions, directory, finishedtask)
{	
	let files = filesystem.readdirSync(directory);
	let outfilekey = "outFile";
	console.log("found " + files.length + " entrypoints to bundle.");

	async.eachSeries(files, (file, continueloop) => {
		console.log("processing " + file + " into a bundle.");
		let buildfilecomponents = file.split(".");		
		parceloptions[outfilekey] = buildfilecomponents[0] + ".js";
		let absolutelocation = path.join(directory, file);
		let bundler = new parcel(absolutelocation, parceloptions);
		let newpath = path.join(directory, parceloptions[outfilekey]);
		
		bundler.bundle()
		.then(function (passpromise, reject) {					
			console.log("waiting for bundle to exist...");

			let fileexists = false;

			while(fileexists == false)
			{
				fileexists = filesystem.existsSync(newpath);

				if (fileexists)
				{
					console.log("bundle exists.");
					continueloop();
				}
			}
		});
	},
	function onfinished(){
		finishedtask();
	});			
}

