heroku ps:scale web=1 --app moonmachine-staging
git push moonmachine-staging master
$promotionverdict = Read-Host -Prompt 'promote to production? [y/n]'

if ($promotionverdict -eq 'y')
{    
    heroku pipelines:promote --app moonmachine-staging --to moonmachine
    heroku ps:scale web=0 --app moonmachine-staging
    Read-Host -Prompt 'script completed'
    
}

else
{
    Exit-PSHostProcess
}