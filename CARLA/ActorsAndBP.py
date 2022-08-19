import random 
import carla

"""
2. Actors and blueprints
"""
# 2.1 Blueprints:
# actors: vehicles and walkers, sensors and traffic signals, lights and spectator
blueprint_library = world.get_actor_library()
# controller.ai.walker
# sensors.camera.depth
# sensors.camera.dvs
# sensors.camera.rgb
# sensors.camera.semantic_segmentation
# sensors.lidar.ray_cast
# sensors.lidar.ray_cast_semantic
# sensors.other.collision
# sensors.other.gnss
# sensors.other.imu
# sensors.other.lane_invasion
# sensors.other.obstacle
# sensors.other.radar
# sensors.other.rss
# static.prop
# vehicle.bh/audi/bmw/chevrolet/citroen/carlamotors/dodge/ford/tesla/volkswagen../(type)
# walker.pedestrian.xxxx

# Blueprints have an ID to identify them and the actors spawned with it. 
# The library can be read to find a certain ID, choose a blueprint at random, or filter results using a wildcard pattern.

# find a specific blueprint
collision_sensor_bp = blueprint_library.find("sensor.other.collision")
# choose a vehicle blueprint at random
vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))

# Besides that, each carla.ActorBlueprint has a series of carla.
# ActorAttribute that can be get and set.
is_bike = [vehicle.get attribute('number_of_wheels') == 2]
if (is_bike):
    vehicle.set_attribute('color','255,0,0')

# Attributes have an carla.ActorAttributeType variable. It states its type from a list of enums.
# Also, modifiable attributes come with a list of recommended values. 
for attr in blueprint:
    if attr.is_modifiable:
        blueprint.set_attribute(attr.id,random.choice(attr.recommended_values))

# 2.2 Actor life cycle

# 2.2.1 Spawning and keeping track(world object in response)
# two way of spawn
spawn_actor()  # raise an exception if fails
try_spawn_actor() # return None if fails

# carla.Transform stating a location and rotation for the actor
transform = Transform(Location(x=230, y=195, z=40), Rotation(yaw=180))  
# (pitch,yaw,roll) in CARLA and (roll, pitch, yaw) in UE4
actor = world.spawn_actor(blueprint,transform)
map.get_spawn_points() # for vehicles. Return a list of recommended spawning points
spawn_points = world.get_map().get_spawn_points()
# world.get_random_location() for walkers. Return a random point on the sidewalks.
spawn_point = carla.Transform()
spawn_point.location = world.get_random_location_from_navigation()

# an actor an be attached to another one, useful for sensors. carla.AttachmentType
camera = world.spawn_actor(camera_bp, relative_transform, attach_to=my_vehicle, carla.AttachmentTypr.Rigid)
# When spawning attached actors, the transform provided must be relative to the parent actor. 
actor_list = world.get_actors()
actor = actor_list.find(id)
for speed_sign in actor_list.filter("traffic.speed_limit.*"):
    print(speed_sign.get_location())
    
# 2.2.2 Handling (carla.Actor)

print(actor.get_acceleration())
print(actor.get_velocity())
location = actor.get_location()
location.z +=10.0
actor.set_location(location)
actor.set_simulate_physics(False)  # Freeze = True
# Besides that, actors also have tags provided by their blueprints. 
# These are mostly useful for semantic segmentation sensors. 
destroyed_successful = actor.destroy()

# 2.3 Type of actors
# 2.3.1 Sensors
camera_bp = blueprint_library.find("sensor.camera.rgb")
camera = world.spawn_actor(camera_bp, relative_transform, attach_to=my_vehicle)
camera.listen(lambda image: image.save_to_disk("output/%06d.png"%image.frame))
# Sensors have blueprints too. Setting attributes is crucial.
# Most of the sensors will be attached to a vehicle to gather information on its surroundings.
# Sensors listen to data. When data is received, they call a function described with a Lambda expression (6.13 in the link provided).

# 2.3.2 Spectator
spectator = world.get_spectator()
transform = vehicle.get_transform()
spectator.set_transform(carla.Transform(transform.location+carla.Location(z=50),carla.Rotation(pitch=-90)))

# 2.3.3 Traffic signs and lights  (with IDs)
# Only stops, yields and traffic lights are considered actors in CARLA so far. 
# The rest of the OpenDRIVE signs are accessible from the API as carla.Landmark.
# Traffic signs are not defined in the road map itself, as explained in the following page. 
# Instead, they have a carla.BoundingBox to affect vehicles inside of it.
if vehicle_actor.is_at_traffic_light():
    traffic_light = vehicle_actor.get_traffic_light()
    
# change a light to green
if traffic_light.get_state()==carla.TrafficLightState.Red:
    traffic_light.set_state(carla.TrafficLightState.Green)
    traffic_light.set_set_green_time(4.0)

# 2.3.4 Vehicles (carla.Vehicle)

# carla.VehicleControl
vehicle.apply_control(carla.VehicleControl(throttle=1.0,steer=-1.0))
# carla.VehiclePhysicsControl: GearPhysicsControl, WheelPhysicsControl
vehicle.apply_physics_control(carla.VehiclePhysicsControl(max_rpm=5000.0, 
                                                        center_of_mass=carla.Vector3D(0.0,0.0,0.0),
                                                        torque_curve=[[0,400],[5000,400]]))
# carla.BoundingBox encapsulating Vehicles
box = vehicle.bounding_box
print(box.location)
print(box.extent)

# The physics of vehicle wheels can be improved by enabling the sweep wheel collision parameter.
# The default wheel physics uses single ray casting from the axis to the floor for each wheel but when sweep wheel collision is enabled,
# the full volume of the wheel is checked against collisions. 
# It can be enabled as such:

physics_control = vehicle.get_physics_control()
physics_control.use_sweep_wheel_collision = True
vehicle.apply_physics_control(physics_control)

# Vehicles include other functionalities unique to them:
# "Autopilot mode" will subscribe a vehicle to the Traffic Manager to simulate real urban conditions. 
# This module is hard-coded, not based on machine learning. 
vehicle.set_autopilot(True)
# Vehicle lights have to be turned on and off by the user. Each vehicle has a set of lights listed in carla.VehicleLightState.
# Turn on position lights
current_lights = carla.VehicleLightState.NONE
current_lights |= carla.VehicleLightState.Position
vehicle.set_light_state(current_lights)

# carla.Walker work in a similar way as vehicles do. Control over them is provided by controllers.

# carla.WalkerControl moves the pedestrian around with a certain direction and speed. It also allows them to jump.
# carla.WalkerBoneControl provides control over the 3D skeleton. This tutorial explains how to control it.
# Walkers can be AI controlled. They do not have an autopilot mode. carla.WalkerAIController

walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
world.SpawnActor(walker_controller_bp, carla.Transform(), parent_walker)
# Each AI controller needs initialization, a goal and, optionally, a speed. Stopping the controller works in the same manner. 
ai_controller.start()
ai_controller.go_to_location(world.get_random_location_from_navigation())
ai_controller.set_max_speed(1 + random.random())  # Between 1 and 2 m/s (default is 1.4 m/s).
ai_controller.stop()
# To destroy AI pedestrians, stop the AI controller and destroy both, the actor, and the controller. 
