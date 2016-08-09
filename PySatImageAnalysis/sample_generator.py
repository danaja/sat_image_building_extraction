# -*- coding: utf-8 -*-
#Used to generate positive building samples from google satellite images
#based on OSM building polygons in geojson format
#
#Note 1: Accuracy of OSM building polygons may vary
#Note 2: Requires downloaded google satellite images(tiles) to
#        have the following file name structure
#        part_latitude_of_center_longitude_of_center.png
#        This code was tested with tiles downloaded using
#        https://github.com/tdeo/maps-hd
#Note 3: OSM building data downloaded from
#        mapzen.com/data/metro-extracts/
#@Author Danaja Maldeniya


from  osgeo import ogr
import os
import geoutils
import image_utils as imu
import cv2
import json
import numpy as np

map_zoom = 19
tile_size = 600

driver = ogr.GetDriverByName('ESRI Shapefile')
shp = driver.Open(r'/home/danaja/Downloads/colombo_sri-lanka.imposm-shapefiles (2)/colombo_sri-lanka_osm_buildings.shp')

layer = shp.GetLayer()
spatialRef = layer.GetSpatialRef()
print spatialRef

#Loop through the image files to get their ref location(center) latitude and longitude
tile_dir="/home/danaja/installations/maps-hd-master/bk3/images-st"
tiles = os.listdir(tile_dir)

#positive sample generation
#==============================================================================
# for tile in tiles:
#      tile_name = tile.replace(".png","")
#      print(tile)
#      center_lat = float(tile_name.split("_")[1])
#      center_lon = float(tile_name.split("_")[2])
#      extent = geoutils.get_tile_extent(center_lat,center_lon,map_zoom,tile_size)
#      layer.SetSpatialFilterRect(extent[2][1],extent[2][0],extent[1][1],extent[1][0])
#      print("feature count: "+str(layer.GetFeatureCount()))
#      print(tile_dir+"/"+tile)
#      image = cv2.imread(tile_dir+"/"+tile)
#      b_channel, g_channel, r_channel = cv2.split(image)
#      alpha_channel = np.array(np.ones((tile_size,tile_size )) * 255,dtype=np.uint8) #creating a dummy alpha channel image.
#      image= cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
#      i = 0
#      for feature in layer:
#          coordinates = []
#          geom = feature.GetGeometryRef()
#          geom = json.loads(geom.ExportToJson())
#
#          for coordinate in geom['coordinates'][0]:
#              pixel = geoutils.get_pixel_location_in_tile_for_lat_lon( \
#              coordinate[1],coordinate[0],center_lat,center_lon,map_zoom,tile_size)
#              if len(coordinates) == 0:
#                  minx = pixel[0]
#                  miny = pixel[1]
#                  maxx = pixel[0]
#                  maxy = pixel[1]
#              minx = min(minx,pixel[0])
#              maxx = max(maxx,pixel[0])
#              miny = min(miny,pixel[1])
#              maxy = max(maxy,pixel[1])
#              coordinates.append(tuple(reversed(pixel)))
#
#          mask = np.zeros(image.shape, dtype=np.uint8)
#          roi_corners = np.array([coordinates], dtype=np.int32)
#          channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
#          ignore_mask_color = (255,)*channel_count
#          cv2.fillPoly(mask, roi_corners, ignore_mask_color)
#          masked_image = cv2.bitwise_and(image, mask)
#          masked_image = masked_image[minx:maxx,miny:maxy]
#          cv2.imwrite("positive/"+tile_name+"_"+str(i)+".png",masked_image)
#          i=i+1
#      layer.SetSpatialFilter(None)
#
#==============================================================================

#negative sample generation
min_size = 80
max_size = 100

for tile in tiles:
     tile_name = tile.replace(".png","")
     print(tile)
     center_lat = float(tile_name.split("_")[1])
     center_lon = float(tile_name.split("_")[2])

     extent = geoutils.get_tile_extent(center_lat,center_lon,map_zoom,tile_size)
     layer.SetSpatialFilterRect(extent[2][1],extent[2][0],extent[1][1],extent[1][0])

     if layer.GetFeatureCount() > 0:
         layer.SetSpatialFilter(None)
         attempt = 0
         success = 0

         while (attempt <100 and success <20):
             box =imu.generate_random_box(tile_size,min_size,max_size)
             nw_corner = geoutils.get_lat_lon_of_point_in_tile(box[0],box[1],center_lat,center_lon,map_zoom,tile_size)
             se_corner = geoutils.get_lat_lon_of_point_in_tile(box[2],box[3],center_lat,center_lon,map_zoom,tile_size)
             layer.SetSpatialFilterRect(nw_corner[1],se_corner[0],se_corner[1],nw_corner[0])
             fCount = layer.GetFeatureCount()
             if fCount >0:
                 continue
             else:
                 image = cv2.imread(tile_dir+"/"+tile)
                 bld = image[int(box[1]):int(box[3]), \
                         int(box[0]):int(box[2])]
                 cv2.imwrite("negative/"+tile_name+"_"+str(success)+".png",bld)
                 success = success+1

             layer.SetSpatialFilter(None)
             attempt = attempt +1







