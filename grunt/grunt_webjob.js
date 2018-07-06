const parcel = require("parcel");
const async = require("async");
const path = require("path");
const filesystem = require("fs");

//pipeline
const INPUTFOLDERREL = "../app/front/";
const OUTPUTFOLDERREL = "../app/static_pipeline/";
const OUTPUTFOLDERABS = path.join(__dirname, OUTPUTFOLDERREL);
const OUTPUTJAVASCRIPTFOLDER = OUTPUTFOLDERABS + "scripts/";

//parcel
const BINDERSFOLDEREL = "custom/binders";
const INPUTBUNDLEFOLDER = OUTPUTJAVASCRIPTFOLDER + BINDERSFOLDEREL;

const jsextension = ".js";

module.exports = function(grunt) //using the nodejs module format
{	
	let configobject = {
		pkg: grunt.file.readJSON('../package.json'),

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
	
	require('load-grunt-tasks')(grunt, {
		requireResolution: true //helps to find the node_modules folder in a different dir.
	});
	
	grunt.registerTask("pipeline", "description", pipelinetask);
	grunt.registerTask("parcel", "description", parceltask);
	
	grunt.registerTask("development", ["pipeline", "parcel:true"]);
	grunt.registerTask("production", ["pipeline", "babel", "parcel:false"]);
};

function SetPaths(configobject)
{
	let alljsfiles = { //dynamic file mappings
		expand: true,
		cwd: OUTPUTJAVASCRIPTFOLDER,
		src: ["**/*.js"],
		dest: OUTPUTJAVASCRIPTFOLDER	
	};
	configobject.babel.production.files = [alljsfiles];
	return configobject;
}

function pipelinetask()
{
	deleteoldpipeline();
	collectfronttopipeline();
}

function parceltask(debugmodebool) 
{	
	let done = this.async(); //grunt specific command for making an asynchronous task.	
	renamebundlestomin();	
	buildbundles(debugmodebool, done);
}

function deleteoldpipeline()
{
	console.log("___________________________________")
	console.log("beginning " + deleteoldpipeline.name);

	foldertraverser(OUTPUTFOLDERREL, function onfile (currentdirectory, currentfile)
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

	foldertraverser(INPUTFOLDERREL, function onfile (currentdirectory, currentfile, addeddirectories) 
	{
		let itemsfullpath = path.join(__dirname, currentdirectory, currentfile);	
		let itemsoutputpath = path.join(OUTPUTFOLDERABS, addeddirectories, currentfile);
		console.log("current path: " + itemsfullpath);
		console.log("destination path: " + itemsoutputpath);			
		console.log("copying...");
		filesystem.copyFileSync(itemsfullpath, itemsoutputpath);		
	},
	function ondirectory(currentdirectory, currentfile, addeddirectories)
	{
		let itemsoutputdir = path.join(OUTPUTFOLDERABS, addeddirectories, currentfile);	
		
		if (filesystem.existsSync(itemsoutputdir) === false)
		{
			console.log("creating mirror directory: " + itemsoutputdir);
			filesystem.mkdirSync(itemsoutputdir);			
		}
	});
}

//callbacks are given currentdirectory, currentfilename, addeddirectories.
//currentdirectory must be relative to the location of this grunt file.
//onnewdirectory can be null.
function foldertraverser(relativedirectory, onfile, onnewdirectory)
{
	const standardpreprend = "/";
	const addedindex = 3;
	const isnotgiven = () => arguments[addedindex] !== undefined && typeof (arguments[addedindex]) === "string";
	let addeddirectoriesstr = isnotgiven() ? arguments[addedindex] : ""; //access an overload argument. hopefully not given by the invoker.
	console.log("NEW TRAVERSAL");
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
			foldertraverser(itemsrelativepath, onfile, onnewdirectory, nextlayeradditions);
		}
	}
}

function renamebundlestomin()
{
	console.log("renaming bundle inputs so that source maps may work.");
	let files = filesystem.readdirSync(INPUTBUNDLEFOLDER);

	for (let i = 0; i < files.length; i++)
	{
		console.log("renaming " + files[i]);
		let filenamecomponents = files[i].split(".");
		let newpath = INPUTBUNDLEFOLDER + "/" + filenamecomponents[0] + ".build" + jsextension;
		let oldpath = path.join(INPUTBUNDLEFOLDER, files[i]);
		filesystem.renameSync(oldpath, newpath);
	}
}

function buildbundles(debugmodebool, finishedtask)
{	
	console.log("debugmodebool type: " + typeof(debugmodebool))
	let shouldminify = debugmodebool === "false" ? true : false; //if in debug mode, dont minify
	let shouldgensourcemaps = shouldminify === false; //if in debug mode, generate source maps

	let parceloptions = {
		outDir: INPUTBUNDLEFOLDER,
		cache: false,
		logLevel: 3,
		minify: shouldminify,
		sourceMaps: shouldgensourcemaps,
		watch: false
	};
	console.log("parcel minify: " + parceloptions["minify"]);
	console.log("parcel sourcemaps: " + parceloptions["sourceMaps"]);

	let possibleherokuport = process.env.PORT;
	let hmrportkey = "hmrPort";

	if (possibleherokuport != null)
	{
		console.log("heroku port found. setting parcel port to " + possibleherokuport);
		parceloptions[hmrportkey] = possibleherokuport;
	}

	let files = filesystem.readdirSync(INPUTBUNDLEFOLDER);
	let outfilekey = "outFile";
	console.log("found " + files.length + " entrypoints to bundle.");

	async.eachSeries(files, (file, continueloop) => {
		console.log("processing " + file + " into a bundle.");
		let buildfilecomponents = file.split(".");		
		parceloptions[outfilekey] = buildfilecomponents[0] + jsextension;
		let absolutelocation = path.join(INPUTBUNDLEFOLDER, file);
		let bundler = new parcel(absolutelocation, parceloptions);
		let newpath = path.join(INPUTBUNDLEFOLDER, parceloptions[outfilekey]);
		
		bundler.bundle()
		.then(() => {					
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
