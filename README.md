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
    

    
## Use

    $ generate db


## Note

Following users will be always available to interact with RapidPRO
    
- One system superuser `superuser` (password `123`) 
- One "all organizations" admin `admin` (password `123`)
