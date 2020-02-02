﻿Write-Host 'starting the staging site.'
heroku ps:scale web=1 --app moonmachine-staging
Write-Host 'deploying to staging site.'
git push moonmachine-staging master
$promotionverdict = Read-Host -Prompt 'promote to production? [y/n]'

if ($promotionverdict -eq 'y')
{    
    heroku pipelines:promote --app moonmachine-staging --to moonmachine    
    Read-Host -Prompt 'script completed'    
}
heroku ps:scale web=0 --app moonmachine-staging
Exit-PSHostProcess