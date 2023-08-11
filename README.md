# Lego_vault
This project builds on the Lego Spike lesson: [Keep It Safe](https://education.lego.com/en-au/lessons/prime-kickstart-a-business/keep-it-safe/). 

![Image of lesson 7 from Lego Education](images/Lesson_7.png "Lego Education's lesson 7")


The project also makes use of the [Raspberry Pi Build Hat](https://www.raspberrypi.com/products/build-hat/).
<p align="center">
  <img src="images/build-hat.jpg" alt="Picture" width="400" style="margin: 0 auto" /></img>
</p>


# Setting up the Bank Vault
## Creating virtual encironment
### Linux (Raspberry Pi OS)
Use the venv module to create a virtual environment
```
python3 -m venv .venv
```
Then, activate the environment:
```
. ./.venv/bin/activate
```
`. ./.venv/bin/activate`

#### Installing the dependencies
With the virtual environment activated, install the dependencies

```
pip install flask
pip install buildhat
```

Example on the Raspberry Pi:

```
(venv)pi@raspberrypi:~/LEGO $ pip install flask, buildhat
```

Before we can run the server, we need to create (or download) a ```.env``` file. This file contains our pin number and should be formatted like so; `pin='1234'`.
The project contains an app.py file, which is the Lego Vault server. Run it with the following command:

```
flask run --host=0.0.0.0
```


# Setting up the Clients Brute Forcing script
## Linux

### Creating virtual encironment
Use the venv module to create a virtual environment

```
python3 -m venv .venv

. ./.venv/bin/activate
```

##### Installing the dependencies
With the virtual environment activated, install the dependencies

```
pip install requests
```

##### Running the script
```
python3 brute_force.py <Bank Vault IP> <port>
```

## Windows

### Creating virtual encironment
Use the venv module to create a virtual environment

```
py -m venv .venv

.venv\Scripts\activate
```

##### Installing the dependencies
With the virtual environment activated, install the dependencies

```
pip install requests
```

##### Running the script
```
py brute_force.py <Bank Vault IP> <port>
```
