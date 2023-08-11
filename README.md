# Lego_vault
This project builds on the Lego Spike lesson: [Keep It Safe](https://education.lego.com/en-au/lessons/prime-kickstart-a-business/keep-it-safe/). 

![Image of lesson 7 from Lego Education](images/Lesson_7.png "Lego Education's lesson 7")


The project also makes use of the [Raspberry Pi Build Hat](https://www.raspberrypi.com/products/build-hat/).
<p align="center">
  <img src="images/build-hat.jpg" alt="Picture" width="400" style="margin: 0 auto" /></img>
</p>

## Creating virtual encironment
Use the venv module to create a virtual environment
`python3 -m venv .venv`
Activate it with
#### Linux
`. ./.venv/bin/activate`
#### Windows
`.venv\Scripts\activate`

### Installing the dependencies
With the virtual environment activated, install the dependencies

`pip install flask

pip install buildhat`

Example on the Raspberry pi:

```(venv)pi@raspberrypi:~/LEGO $ pip install flask, buildhat```

The project contains an app.py file, which is the Lego Vault server. Run it with the following command:

`flask run --host=0.0.0.0`
