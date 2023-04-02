# Octopus Energy Agile lowest n'th rate 

Simple python flask app to query the [Octopus Energy API](https://octopus.energy/dashboard/new/accounts/personal-details/api-access) and calculate the lowest n'th number of half hour time slots of energy and expose this value to a url that Homeassistant can injest as a sensor and use as an automation to switch on devices. This differs from the HACS agile integration as the slots don't have to be in a block but can be anywhere in the 24 hour period running 16:00 - 16:00. 

Use octopusagile.conf to set your OctopusEnergy Apikey, Agile URL and slots (the number of halfhour slots you need i.e. 4 hours: "slots = 8")

Run the application by using python octopusagile.py

Test it works by visiting http://localhost:5000/ on the same host and the result should be the nth lowest rate over the next 24 hours.

Edit your hommeassistant configuration to add a new Rest sensor to query this periodically...

Example template sensor for configuration.yaml

```
- platform: rest
  name: lowest_nth_electric
  unit_of_measurement: "GBP/kWh"
  resource: http://<hostdns-ipaddress>:5000
  scan_interval: 1200
```

Then setup an automation to compare the current rate against this lowest nth rate to then switch on a device...

Example Automation:
```
  alias: Battery Chager On if Rate is cheapest nth slots
  description: ""
  trigger:
  - platform: template
    value_template: >-
      {{ states('sensor.octopus_energy_electricity_xxxxxxxxxx_current_rate') | float
      <= states('sensor.lowest_nth_electric') | float }}
  condition: [] 
  action:
  - type: turn_on
  - deviceid: xxxxxx
```
