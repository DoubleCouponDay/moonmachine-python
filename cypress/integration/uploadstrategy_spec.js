describe("uploadstrategy", () => {
    it("werks", () => {
        cy.visit("/admin/porfolio")
            .wait(3000)
            .then(() => {
                cy.get("#authfilebox")
                    .click()
            })
            .then(() => {
                cy.get("button")
                    .contains("Upload")
                    .click()
            })
            .then(() => {
                cy.get("#dooting")
                    .should("")
            })
            .then(() => {
                cy.server()
                .wait()
            })
            .then(() => {
                cy.get("#dooting")
                    .should("not.be.visible");
            })
    });
});