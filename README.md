# octopus agile lowest nth rate 
Octopus Energy Agile lowest nth rate

Simple python flask app to output the lowest nth rate of electric for the current day to emable a Homeassistant automation to switch on devices. This differs from the HACS agile integration as the slots don't have to be in a block but can be anywhere in the 24 hour period running 16:00 - 16:00

Example template sensor for configuration.yaml

```
- platform: rest
  name: lowest_nth_electric
  unit_of_measurement: "GBP/kWh"
  resource: http://<hostdns-ipaddress>:5000
  scan_interval: 1200
```
  
Then setup an automation to compare the current rate against the lowest nth rate - e.g.

Example Automation:
```
  alias: Battery Chager On if Rate is cheapest nth slots
  description: ""
  trigger:
  - platform: template
    value_template: >-
      {{ states('sensor.octopus_energy_electricity_xxxxxxxxxx_current_rate') | float
      <= states('sensor.lowest_8th_electric') | float }}
  condition: [] 
  action:
  - type: turn_on
  - deviceid: xxxxxx
```

Use octopusagile.conf to set your OctopusEnergy Apikey and Agile URL
Set the number of halfhour slots you need i.e. 4 hours: "slots = 8"
