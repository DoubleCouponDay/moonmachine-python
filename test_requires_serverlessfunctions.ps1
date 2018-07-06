param ($browser)
Write-Host 'starting the test server.'
cd ./app #fix context bug with python script
$devserverproc = Start-Process ./run_server.ps1 -WindowStyle Minimized -PassThru
cd ../
$waittime = 40
Start-Sleep -Seconds $waittime
Write-Host 'waited' $waittime 'seconds for test server to start.'
Write-Host 'running tests with browser:' $browser
./node_modules/.bin/cypress run --browser $browser
Write-Host 'stopping dev server: (doesnt work)' $devserverproc
Stop-Process -InputObject $devserverproc
Pause