heroku ps:scale web=1 --app moonmachine-staging
git push moonmachine-staging master
Read-Host -Prompt 'press enter when ready to move app to production'
heroku pipelines:promote --app moonmachine-staging --to moonmachine
heroku ps:scale web=0 --app moonmachine-staging
Read-Host -Prompt 'script completed'
