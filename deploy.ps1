heroku ps:scale web=1 --app moonmachine2
git push moonmachine2 master
Read-Prompt -Prompt 'press enter when ready to move app to production'
heroku pipelines:promote --app moonmachine2 --to moonmachine
heroku ps:scale web=0 --app moonmachine2
