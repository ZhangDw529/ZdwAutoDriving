from http import client
import carla
import random

"""
1. World and client
"""

client = carla.Client('localhost', 2000)   # the other is 2001
client.set_timeout(10.0)
world = client.get_world()
print(client.get_available_maps())  
# The client can also get a list of available maps to change the current one. 
# This will destroy the current world and create a new one.
world = client.load_world('Town01')

# actors

## weather
weather = carla.WeatherParameters(
    cloudiness=80.0,
    precipitation=30.0,
    sun_altitude_angle=70.0
)
world.set_weather(weather)
print(world.get_weather())

# preset parameters
world.set_weather(carla.WeatherParameters.WetCloudySunset)
# The weather can be changed in environment.py or dynamic_weather.py
# Night mode starts when sun_altitude_angle < 0, which is considered sunset. 

## Lights
# Streets
# Carla.LightManager
lmanager = world.get_lightmanager()
mylights = lmanager.get_all_lights()

# custom a specific light
light01 = mylights[0]
light01.turn_on()
light01.set_intensity(100.0)
state01 = carla.LightState(200.0, red ,carla.LightGroup.Building,True)
light01.set_light_state(state01)

# custom a group of lights
my_lights = lmanager.get_light_group(carla.LightGroup.Building)
lmanager.turn_on(my_lights)
lmanager.set_color(my_lights, carla.Color(255,0,0))  #rgb
lmanager.set_intensities(my_lights,list_of_intensities)

# Vehicle lights have to be opened by user in cala.VehicleLightState
current_lights = carla.VehicleLightState.NONE
current_lights |=carla.VehicleLightState.Position
vehicle.set_light_state(current_lights)
# Lights can also be set in real time using the environment.py described in the weather section. 


## Debugging
debug = world.debug
debug.draw_box(carla.BoundingBox(actor_snapshot.get_transform().location,carla.Vector3(0.5,0.5,2)),
               actor_snapshot.get_transform().rotation, 0.05, carla.Color(255,0,0,0),0)


## world snapshot
world.snapshot = world.get_snapshot()
# A carla.WorldSnapshot contains a carla.Timestamp and a list of carla.ActorSnapshot. 
# Actor snapshots can be searched using the id of an actor.
# A snapshot lists the id of the actors appearing in it. 
timestamp = world.snapshot.timestamp
for actor_snapshot in world.snapshot:
    actual_actor=world.get_actor(actor_snapshot.id)
    actor_snapshot.get_transform()
    actor_snapshot.get_velocity()
    actor_snapshot.get_angular_velocity()
    actor_snapshot.get_acceleration()
    
actor_snapshot = world.snapshot.find(actual_actor.id)

## WorldSettings Advanced in carla.WorldSettings