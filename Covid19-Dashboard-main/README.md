
# Covid19 Dashboard Netherlands
A [Covid19 dashboard](http://covid19dashnetherlands.herokuapp.com/) displaying live data for the Netherlands, made with Dash Plotly.

## Usage

In its current form it is configured to work on a Heroku webserver, together with a Heroku Postgres Database. To run this project locally,
you should use the supplied docker-compose.yml file to launch the application as a docker container.

```bash
cd <YOUR PROJECT FOLDER>
docker-compose up --build
```

For this to work locally, you should comment the file locations which reference to the Heroku Postgres Database and uncomment the file 
locations which contain the local filepath in the volume which is specified in the docker-compose.yml file.

Also, the 'Dockerfile' in the app folder should be changed with 'tempDockerfile_localGunicorn.txt' to run locally.

```python
# Comment these
DB_URL = os.environ.get('DATABASE_URL')
DB_URL = DB_URL.replace('postgres', 'postgresql')
df_data = load_data(DB_URL)

# Uncomment these
#filepath = './files/final_df.csv'
#df_data = pd.read_csv(filepath, sep=',')
```

This should be done in app.py, covidcijfers.py, vaccinatiecijfers.py and dataset.py.


## Installation on Heroku

For now the web application is launched on Heroku by manually creating the images with the docker-compose.yml file. In the future
each push to the github main branch will automatically redeploy the update application by using the heroku.yml file.

To push and release the created images to Heroku, make sure to have the Heroku Cli installed. You also need to set the 
stack type of your application to container with the following command

```bash
heroku stack:set container
```

Perform the following commands in the command window one by one.

```bash
heroku login
heroku container:login

***find image id's***
docker image ls

docker tag <image_id1> registry.heroku.com/<your app name>/worker
docker push registry.heroku.com/<your app name>/worker

docker tag <image_id2> registry.heroku.com/<your app name>/web
docker push registry.heroku.com/<your app name>/web

heroku container:release worker --app <your app name>
heroku container:release web --app <your app name>
```



## License
[MIT](https://choosealicense.com/licenses/mit/)
