README


Dependencies:

*  Python 3.7 or above
*  Django 3 or above
*  Docker Desktop -- available at https://www.docker.com/products/docker-desktop -- 
    or other way of running a redis server
    
    
    
To run game:
1. Start Docker Desktop

2. Run the following command to start a redis server on port 6379:
    docker run -p 6379:6379 -d redis:5

3a. (To run exclusively on your computer) While in FindYourWords directory, run:
    python3 manage.py runserver

3b. (To run on local network) While in FindYourWords directory, run:
    python3 manage.py runserver [network ip of your computer]
    
4a. If you used 3a, navigate in browser to 127.0.0.1

4b. If you used 3b, navigate in browser to your local ip address 
    (able to be done on other computers in your network also)
