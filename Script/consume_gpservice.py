#*******************************************************************************************************************#
#                                                                                                                   #
#                 This script demonstrates how to consume a geoprocessing service using arcpy functions             #
#                                                                                                                   #
#                                       2022 Developer Summit    ESRI GP Service team                               #
#                                                                                                                   #
#*******************************************************************************************************************#

import arcpy
import config
import os
import sys
import time


arcpy.env.overwriteOutput = True
ws = arcpy.env.workspace = config.workspace
hs_output = os.path.join(config.scratchworkspace, 'hotspotoutput')

try:
    # Import toolbox
    arcpy.ImportToolbox('https://{0}/arcgis/services;hotspotgpservice;{1};{2}'
                        .format(config.standaloneserver, config.sausername, config.sapassword))
    
    # Run the tool and get the job ID
    inputCalls = arcpy.MakeFeatureLayer_management(
        'https://oct1091cert4.westus.cloudapp.azure.com/server/rest/services/Hosted/callsFS/FeatureServer/0')
    result = arcpy.hotspotgpservice.hotspotscript(calls = inputCalls, rastersize = 'stowe_lyr')
    
    while result.status != 4:
        time.sleep(0.2)
    
    # Save the result at disk space    
    routput = result.getOutput(0)
    arcpy.CopyFeatures_management(routput, hs_output)
    
    print("Consume gp service successfully. gp service = {} ".format(result))
    print("Copied data on disk is at {}".format(hs_output))
except:
    print("Unexpected error during consuming web tool: ", sys.exc_info())
