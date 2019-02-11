# rapidpro-datagen


RapidPro sample data generator.

## Prerequisites

 - pipenv (better with pipsi)
 - npm
 
 
### NOTE: 
    
> Due some conflicts in the RapidPRO requirements, that prevent the creation of a 
> replicabile and predicibile environment, it is not possible to install rapidpro 
> using pipenv.
> We still use pipenv to be ready if/when RapidPRO requirements conflicts will be solved. 


## Install

Set `DATABASE_URL` environment variable to reflect your postgres database
    
    $ export DATABASE_URL=postgres://postgres:@127.0.0.1:5432/rapidpro

Clone the repo and setup the virtualenv

    $ git clone https://github.com/unicef/rapidpro-datagen.git datagen
    $ cd datagen
    $ pipenv shell
    $ make develop
    $ pipenv shell
    
 
## HELP
    $ generate --help
    Usage: RapidPro Data Generator [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.
    
    Commands:
      db      generate data
      status  display database numbers
      zap     empty database
      
### db
    $ generate db --help
    Usage: RapidPro Data Generator db [OPTIONS]
    
      generate data
    
    Options:
      -v, --verbosity INTEGER
      --zap                    Erase all data first
      --atomic                 Use single transaction
      --append                 do not create new organizations. Append new data to existing
      --processes INTEGER      number of processes to use
      --seed INTEGER           initial pk value for numbers
      --organizations INTEGER  Number od Organizations to create
      --channels INTEGER       Minimum number of Channels to create
      --contacts INTEGER       Minimum number of Contacts to create
      --archives INTEGER       Minimum number of Archive to create
      --flows INTEGER          Minimum number of Flow to create
      --broadcasts INTEGER     Minimum number of Broadcasts to create
      --base-email EMAIL       Base GMail addres to use for email generation
      --admin-email EMAIL      Alll Organizanizations admin's email
      --superuser-email EMAIL  System superuser email
      --help                   Show this message and exit.   
      
      
       
## Note

Following users will be always available to interact with RapidPRO
    
- One system superuser `superuser` (password `123`) 
- One "all organizations" admin `admin` (password `123`)

- Multiprocessing does not work on some platform, due postgres `libpq` issues. 
Use `--processes=1` if any problem 
