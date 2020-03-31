# mytank

Mytank is a raspberry pi zero w based tank controller.  It can be used in conjuntion with smart devices to control and monitor aquariums, terrariums, ponds and any other type of tank you might want to monitor.  Mytank is built with opensource components and is intended to be completely opensouce.

## Getting Started

To get started you will need to aquire and assemble all of the components in the Build List and then assemble them according to the instructions.  There is minimal soldering needed and should be able to be accoplished by a noviced solderer.  

### Build List

Here are the components you will need to build the device

* Raspberry pi zero w
* SHT-20 or SHT-30 temperature/humidity sensor
* DS18B20 1-Wire temperature sensor
* (1) 4.7k ohm resistor
* micro sd card - (we recommend a 16 gig)

### Build Instructions


### Build Base SD Card

You will need to create a typical raspian install for raspberry pi zero.  This section will walk you though doing a headless install of raspian.

1. Download latest raspian lite image from: https://www.raspberrypi.org/downloads/raspbian/
2. Burn the image to your SD card.  (We use a tool like Etcher, but there are others) https://www.balena.io/etcher/
3. Configure wifi
  a. Create a wpa_supplicant.conf file and supply your wifi configuration. https://linux.die.net/man/5/wpa_supplicant.conf
  b. Copy the wpa_supplicant.conf file to the boot partition on your SD card
4. Enable ssh by creating a blank ssh file on the boot partition of your SD card
  * ```touch /Volumes/boot/ssh```


### Installing


Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

