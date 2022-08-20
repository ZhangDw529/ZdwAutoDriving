"""
4. Sensors and Data
(Crucial)
"""

# 4.1 Sensors step by step
# Sensors are special type of actor able to measure and stream data
# Data are inherited from general carla.SensorData
# When do sensors retrieve data ?
# Either on every simulation step or when a certain event is registered. Depend on the type of sensor.
# How do sensors retrieve data ?
# Every sensor has listen() method to recieve and manage the data.

# 4.1.1 Setting
# Blueprint for sensors
blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
blueprint.set_attribute('image_size_x','1920')
blueprint.set_attribute('image_size_y','1080')
blueprint.set_attribute('fov','110')
blueprint.set_attribute('sensor_tick','1.0')

# 4.1.2 Spawning
# attachment_to and attachment_type, are crucial
# Sensors should be attached to a parent actor, usually a vehicle, to follow it around and gather the information
# The attachment type will determine how its position is updated regarding said vehicle. 
# Rigid attachment. Movement is strict regarding its parent location. This is the proper attachment to retrieve data from the simulation. 
# SpringArm attachment. Movement is eased with little accelerations and decelerations.
transform = carla.Transform(carla.Location(x=0.8,z=1.7))
sensor = world.spawn_actor(blueprint, transform, attach_to=my_vehicle)
# When spawning with attachment, location must be relative to the parent actor. 


# 4.1.3 Listening
# Every sensor has a listen() method. This is called every time the sensor retrieves data. 
# The argument callback is a lambda function. It describes what should the sensor do when data is retrieved. This must have the data retrieved as an argument. 
sensor.listen(lambda data: do_something(data))

# This collision sensor would print everytime a collision is detected. 
def callback(event):
    for actor_id in event:
        vehicle = world_ref().get_actor(actor_id)
        print('vehicle too close: %s'% vehicle.type_id)

sensor02.listen(callback)

# 4.1.4 Data
frame (int)
timestamp(double)
transform(carla.Transform)  # world reference of the sensor at the time of the measurement
# is_listening is a sensor attribute that enables/disables data listening at will.
# sensor_tick is a blueprint attribute that sets the simulation time between data received. 

# 4.2 Types of Sensors
# 4.2.1 Camera
# Depth, RGB, Optimal Flow, Semantic segmentation, DVS

# 4.2.2 Detectors
# Collision, Lane invasion, Obstacle

# 4.2.3 Other
# GNSS, IMU, LIDAR, RADAR, RSS, Semantic LIDAR