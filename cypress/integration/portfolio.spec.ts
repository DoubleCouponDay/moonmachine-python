describe('portfolio', function () {
    before(function () {

    })

    beforeEach(function () { // events emitted from cy are unsubscribed after each test!
        cy.server()

        cy.fixture('strings.json')
            .as('strings')

        cy.login()

        cy.visit('/admin/portfolio')
            .wait(3000)

        cy.route('/admin/portfolio/**') // cannot occur before cy.server()
            .as('portfolioroute')
    })

    it('uploads strategy', function () {
        cy.server({
            onResponse: function (response) {
                if (response.status !== 200) {
                    throw new Error('xhr response was not successful.');
                }
            }
        })

        cy.on('window:alert', (message) => {
            throw new Error('window alert opened. ' + message);
        })

        cy.get('#authfilebox')
            .then((authfilebox) => {
                cy.addfile(this.strings.goodpath, authfilebox.first()[0])
            })

        cy.get('button')
            .contains('Upload')
            .click()

        cy.get('#dooting')
            .should('be.visible')

        cy.get('#dooting')
            .should('not.be.visible')

        cy.get('#is-compiled')
            .should('contain', 'true')
    });

    it('detects wrong language', function () {
        let alertcount = 0;

        cy.route('http://localhost:8000/admin/portfolio/putstrategy')
            .as('updatestrategy')

        cy.on('window:alert', (message) => {
            console.log('server blocked request successfully!');
            alertcount++;
        })

        cy.get('#authfilebox')
            .then((authfilebox) => {
                cy.addfile(this.strings.badpath, authfilebox.first()[0])
            })

        cy.get('button')
            .contains('Upload')
            .click()

        cy.get('#dooting')
            .should('be.visible')

        cy.get('#dooting')
            .should('not.be.visible')
            .then(() => {
                if (alertcount === 0) {
                    throw new Error('server did not block request!');
                }
            })
    });

    it('detects no file', function () {
        let alertcount = 0;

        cy.get('button')
            .contains('Upload')
            .click()

        cy.get('#dooting')
            .should('not.be.visible')
            .then(() => {
                if (alertcount === 0) {
                    throw new Error('server did not block request!');
                }
            })

        cy.on('window:alert', (message) => {
            console.log('server blocked request successfully!');
            alertcount++;
        })
    })
});