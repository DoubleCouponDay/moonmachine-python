// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
Cypress.Commands.add("login", function() {   
    cy.visit("/admin")
        .get("#id_username")
        .click()
        .type(this.strings.username)

    cy.get("#id_password")
        .click()
        .type(this.strings.password)

    cy.get("#login-form")
        .submit()        
});

Cypress.Commands.add("addfile", function(filepath, filetypeinputelem) {
    cy.fixture(filepath, "base64")
        .then(Cypress.Blob.base64StringToBlob)
        .then((blob) => {
            let file = new File([blob], filepath.split("/").pop());
            let datatransferobj = new DataTransfer();
            datatransferobj.items.add(file); //add does not exist on datatransferobj.files
            filetypeinputelem.files = datatransferobj.files;
        })
});


