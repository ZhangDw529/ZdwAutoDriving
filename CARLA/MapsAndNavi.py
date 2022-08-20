"""
3. Maps and navigation
"""
from pty import spawn
import carla
import client

### OpenDRIVE standard 1.4
# Changing the map    
world = client.load_world("Town01")
print(client.get_available_maps())

## Landmarks
carla.Landmark()
carla.LandmarkOrientation()
carla.LandmarkType()
carla.Waypoint()
carla.Map()
carla.World()
my_waypoint.get_landmarks(200.0,True)

## Waypoints
# Each waypoint contains a carla.
# Transform which states its location on the map and the orientation of the lane containing it. 
# Access lane information from a waypoint
inside_junction = waypoint.is_junction()
width = waypoint.lane_width()
right_lm_color = waypoint.right_lane_marking.color()

## Lanes
lane_type = waypoint.lane_type()
left_lanemarking_type = waypoint.left_lane_marking.type()
lane_change = waypoint.lane_change()

## Junctions
waypoints_junc = my_junction.get_waypoints()

## Environment Objects
world = client.get_world()
env_objs = world.get_environment_objects(carla.CityObjectLabel.Buildings)
building_01 = env_objs [0]
building_02 = env_objs [1]
objects_to_toggle = {building_01.id, building_02.id}
world.enable_environment_objects(objects_to_toggle, False)
world.enable_environment_objects(objects_to_toggle, True)


## Navigation
# navigate through waypoints
next(d)  # check next waypoint in d meters
previous(d)
next_until_lane_end(d) 
previous_until_lane_start(d)
get_right_lane()
get_left_lane()
waypoint = waypoint.next(2.0)

# generating map navigation
map = world.get_map() # map object contains recommended spawn points for the creation of vehicles
spawn_points = world.get_map().get_spawn_points()
# Nearest waypoint in the center of a Driving or Sidewalk lane.
waypoint01 = map.get_waypoint(vehicle.get_location(),project_to_road=True, 
                              lane_type=(carla.LaneType.Driving | carla.LaneType.Sidewalk))

#Nearest waypoint but specifying OpenDRIVE parameters. 
waypoint02 = map.get_waypoint_xodr(road_id,lane_id,s)

# The below example shows how to generate a collection of waypoints to vosualize the city lanes.
# This will create waypoints all over the map, for every road and lane. All of them woll approximately 2 meters apart:
waypoint_list = map.generate_waypoints(2.0)

# generate a minimal graph of road topology
waypoint_tuple_list = map.get_topology()

# convert a carla.Transform to geographical latitude and longitude coordinates
my_geolocation = map.transform_to_geolocation(vehicle.transform)

# save road information in the OpenDRIVE format to disk
info_map = map.to_opendrive()


## Carla maps
# Load layered map for town 01 with minimum layout plus buildings and parked vehicles
world = client.load_world("Town01_Opt",carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)
# toggle all buildings off
world.unload_map_layer(carla.MapLayer.Buildings)
# toggle all buildings on
world.load_map_layer(carla.MapLayer.Buildings)



