const cypress = require("../node_modules/cypress/index");

module.exports = function(grunt) //using the nodejs module format
{	
	let configobject = {
		pkg: grunt.file.readJSON('../package.json')	
	};
    grunt.initConfig(configobject);		

    grunt.registerTask("cypress", "description", function()
    {
        let done = this.async();
        let projectpath = "../cypress.json";
        let cypressconfig = grunt.file.readJSON(projectpath);

        let configwip = {
            browser: 'chrome',
            project: "../",
          };
        configwip["config"] = cypressconfig; 

        cypress.run(configwip)
          .then((results) => {
              console.log("cypress task complete. reading results..");
              console.log(results);

              if (results.failures === 0)
              {
                done();
              }

              else
              {
                  grunt.fail.fatal("cypress found errors! " + JSON.stringify(results));
              }
          });
    });
    grunt.registerTask("default", ["cypress"]);
};