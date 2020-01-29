# Help Select Unit
##### Introduction:


##### Follow steps below to start project:

Step 1: Install Postgesql
```bash    
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

Step 2: Create virtual environment
    
```bash    
virtualenv env -p python3
```

Step 3: Run virtual environment (for linux users)
    
```bash
    source env/bin/activate
```


Step 4: Install requirement packages from requirements.txt  

```bash
 pip install -r requirements.txt
```

    
Step 5: Run project
```bash
python manage.py runserver
```