let parcel = require("parcel");
let async = require("async");
let path = require("path");
let filesystem = require("fs");
let copydir = require("copy-dir");

const inputfolderrel = "../app/front/";
const inputfolderabs =  path.join(__dirname, inputfolderrel);
const outputfolderrel = "../app/static_pipeline/";
const outputfolderabs = path.join(__dirname, outputfolderrel);
const outputjavascriptfolder = outputfolderabs + "scripts/";
const tobundlefolder = outputjavascriptfolder + "custom/binders";

const jsextension = ".js";

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
	
	grunt.registerTask("pipeline", "description", pipelinetask);
	grunt.registerTask("parcel", "description", parceltask);
	
	grunt.registerTask("development", ["pipeline", "parcel:true"]);
	grunt.registerTask("production", ["pipeline", "babel", "parcel:false"]);
};

function SetPaths(configobject)
{
	let alljsfiles = { //dynamic file mappings
		expand: true,
		cwd: outputjavascriptfolder,
		src: ["**/*.js"],
		dest: outputjavascriptfolder	
	};
	configobject.babel.production.files = [alljsfiles];
	return configobject;
}

function pipelinetask()
{

}

function parceltask(debugmodebool) 
{	
	let done = this.async(); //grunt specific command for making an asynchronous task.		
	deleteoldpipeline();
	collectfronttopipeline();
	// renamebundlestomin();
	// buildbundles(done);
}

function deleteoldpipeline()
{
	console.log("___________________________________")
	console.log("beginning " + deleteoldpipeline.name);

	foldertraverser(outputfolderrel, function (currentdirectory, currentfile)
	{
		let itemsfullpath = path.join(__dirname, currentdirectory, currentfile);
		filesystem.unlinkSync(itemsfullpath);
		console.log(itemsfullpath + " deleted.");
	},
	null);
}

function collectfronttopipeline()
{
	console.log("___________________________________")
	console.log("beginning " + collectfronttopipeline.name);

	foldertraverser(inputfolderrel, function onfile (currentdirectory, currentfile, addeddirectories) 
	{
		let itemsfullpath = path.join(__dirname, currentdirectory, currentfile);	
		let itemsoutputpath = path.join(outputfolderabs, addeddirectories, currentfile);
		console.log("current path: " + itemsfullpath);
		console.log("destination path: " + itemsoutputpath);			
		console.log("copying...");
		filesystem.copyFileSync(itemsfullpath, itemsoutputpath);		
	},
	function ondirectory(currentdirectory, currentfile, addeddirectories)
	{
		let itemsoutputdir = path.join(outputfolderabs, addeddirectories, currentfile);	
console.log("outputfolderabs: " + outputfolderabs);
console.log("addeddirectories: " + addeddirectories);
console.log("currentfile: " + currentfile);
		
		if (filesystem.existsSync(itemsoutputdir) === false)
		{
			console.log("creating mirror directory: " + itemsoutputdir);
			filesystem.mkdirSync(itemsoutputdir);			
		}
	});
}

//callbacks are given currentdirectory, currentfilename, addeddirectories.
//currentdirectory must be relative to the location of this grunt file.
//onnewdirectory is optional.
function foldertraverser(relativedirectory, onfile, onnewdirectory)
{
	const standardpreprend = "/";
	const addedindex = 3;
	const isnotgiven = () => arguments[addedindex] !== undefined && typeof (arguments[addedindex]) === "string";
	let addeddirectoriesstr = isnotgiven() ? arguments[addedindex] : ""; //access an overload argument. hopefully not given by the invoker.
	console.log("NEW TRAVERSAL");
console.log("addeddirectoriesstr: " + addeddirectoriesstr);
console.log("relativedirectory: " + relativedirectory);
	let files = filesystem.readdirSync(relativedirectory);

	for (let i = 0; i < files.length; i++)
	{
		let itemsrelativepath = path.join(relativedirectory, files[i]);
		let itemsstatus = filesystem.lstatSync(itemsrelativepath);			

		if(itemsstatus.isFile() === true)
		{
			console.log("current item '" + files[i] + "' is file.");			
			onfile(relativedirectory, files[i], addeddirectoriesstr);
		}

		else if(itemsstatus.isDirectory() === true)
		{
			console.log("current item '" + files[i] + "' is directory.");

			if (onnewdirectory !== null)
			{
				onnewdirectory(relativedirectory, files[i], addeddirectoriesstr);
			}			
			let nextlayeradditions = addeddirectoriesstr + standardpreprend + files[i]; //take a copy since this addition is only relevant to the next layer.			
			foldertraverser(itemsrelativepath, onfile, nextlayeradditions);
		}
	}
}

// function renamebundlestomin()
// {
// 	console.log("renaming bundle inputs so that source maps may work.");
// 	let files = filesystem.readdirSync(tobundlefolder);

// 	for (let i = 0; i < files.length; i++)
// 	{
// 		console.log("renaming " + files[i]);
// 		let filenamecomponents = files[i].split(".");
// 		let newpath = directory + "/" + filenamecomponents[0] + ".build" + jsextension;
// 		let oldpath = path.join(directory, files[i]);

// 		console.log("renameoldpath: " + oldpath);
// 		console.log("renamenewpath: " + newpath);
// 		filesystem.renameSync(oldpath, newpath);
// 	}
// }

// // function buildbundles(directory, finishedtask)
// // {	
// // 	let parceloptions = {
// // 		outDir: directory,
// // 		cache: false,
// // 		logLevel: 3,
// // 		minify: debugmodebool === false,
// // 		sourceMaps: false //todo: set to debugmodebool once issues sorted
// // 	};
// // 	let files = filesystem.readdirSync(directory);
// // 	let outfilekey = "outFile";
// // 	console.log("found " + files.length + " entrypoints to bundle.");

// // 	async.eachSeries(files, (file, continueloop) => {
// // 		console.log("processing " + file + " into a bundle.");
// // 		let buildfilecomponents = file.split(".");		
// // 		parceloptions[outfilekey] = buildfilecomponents[0] + jsextension;
// // 		let absolutelocation = path.join(directory, file);
// // 		let bundler = new parcel(absolutelocation, parceloptions);
// // 		let newpath = path.join(directory, parceloptions[outfilekey]);
		
// // 		bundler.bundle()
// // 		.then(function (passpromise, reject) {					
// // 			console.log("waiting for bundle to exist...");

// // 			let fileexists = false;

// // 			while(fileexists == false)
// // 			{
// // 				fileexists = filesystem.existsSync(newpath);

// // 				if (fileexists)
// // 				{
// // 					console.log("bundle exists.");
// // 					continueloop();
// // 				}
// // 			}
// // 		});
// // 	},
// // 	function onfinished(){
// // 		finishedtask();
// // 	});			
// // }

