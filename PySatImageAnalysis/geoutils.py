# -*- coding: utf-8 -*-
import math

R = 6378137
S = 111320

def get_lat_lon_of_point_in_tile(x,y,center_lat,center_lon,zoom,size):
    r = (math.cos(center_lat*math.pi/180)*2*math.pi*R)/(256*2**zoom)
    dx = x - size/2
    dy = y - size/2
    lat = center_lat - (dy*r)/S
    lon = center_lon + (dx*r)/S
    loc = [lat,lon]
    return loc

#Returns the extents of a map tile based on the lat,lon of the center
#the zoom and tile size(width=height)
def get_tile_extent(center_lat,center_lon,zoom,size):
    nw_corner = get_lat_lon_of_point_in_tile(0,0,center_lat,center_lon,zoom,size)
    ne_corner = get_lat_lon_of_point_in_tile(size,0,center_lat,center_lon,zoom,size)
    sw_corner = get_lat_lon_of_point_in_tile(0,size,center_lat,center_lon,zoom,size)
    se_corner = get_lat_lon_of_point_in_tile(size,size,center_lat,center_lon,zoom,size)

    return [nw_corner,ne_corner,sw_corner,se_corner]

def get_pixel_location_in_tile_for_lat_lon(lat,lon,center_lat,center_lon,zoom,size):
    r = (math.cos(center_lat*math.pi/180)*2*math.pi*R)/(256*2**zoom)
    dx = S*(center_lat-lat)/r
    dy = S*(lon-center_lon)/r
    x = math.floor(dx+(size/2))
    x = min(max(0,x),size)
    y = math.floor(dy+(size/2))
    y = min(max(0,y),size)
    return [x,y]