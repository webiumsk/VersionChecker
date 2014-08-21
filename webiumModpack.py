# -*- coding: cp1250 -*-
# The imports below are required for the ModSettings API.
# You could and should use a try block to do the imports and check if the ModSettingsAPI is installed. Afterwards you can check the API level to check if the features that you want to use are available.
#
# The API level constant was introduced with version 1.1.0, so if it can't be imported, then the API Level is to be considered 0.
#
# Changes:
# 1:
#   - JSON Support
#   - Function Callbacks
#
# 0:
#   - Initial version, only external SWF's supported
import BigWorld
import os
from debug_utils import *
import GUI
import ResMgr
#from helpers import links
import urllib2
from xml.dom.minidom import parseString
from gui.Scaleform.daapi.view.lobby.settings.SettingsWindow import ModSettingsAPI, MODSETTINGS_API_LEVEL
#webium old version checker part 1
latestVersion = 'Unknown'
changelogXml = ' '
changelogXmlCs = ' '
infoXml = 'No news'
infoXmlCs = 'Ziadne novinky'
layoutHeight = 250
try:
    file = urllib2.urlopen('http://pastebin.com/raw.php?i=YjBKf9SR')
    data = file.read()
    file.close()
    dom = parseString(data)
    latestVersion = dom.getElementsByTagName('version')[0].firstChild.data
    changelogXml = dom.getElementsByTagName('changes')[0].firstChild.data
    changelogXmlCs = dom.getElementsByTagName('changescs')[0].firstChild.data
    infoXml = dom.getElementsByTagName('info')[0].firstChild.data
    infoXmlCs = dom.getElementsByTagName('infocs')[0].firstChild.data
    layoutHeight = dom.getElementsByTagName('height')[0].firstChild.data
except:
    LOG_ERROR('Unable to access Remote File')
    
installedVersion = '0.0'
modpackUrl = 'http://www.mywotmods.com/mods/mod-packs/item/10-webium-s-mods-pack'
updateAvailable = ' is available. More info in MENU - Settings - MODS'
upToDate = ' is up to date.'
updateText = ''
xml = ResMgr.openSection('scripts/client/mods/webiumModpack.xml')
if xml is not None:
    installedVersion = xml.readString('version')
    modpackUrl = xml.readString('updateLink')
    updateAvailable = xml.readString('updateAvailable')
    upToDate = xml.readString('upToDate')
    updateText = xml.readString('updateText')
else:
    LOG_ERROR('Unable to load scripts/client/mods/webiumModpack.xml')
#end of webium old version checker part 1 
print "Webium's modpack version checker", MODSETTINGS_API_LEVEL

# This function will be called, after the "Apply" button was clicked
# The function has to be registered with ModSettings.registerFunction() and has to be set as callback in the layout data.
def applyButtonPressed(objName, value):
    print "Webium's modpack: The apply button was clicked, the new values are:", value
    
def buttonPressed(objName, value):
    print "The button", objName, "was clicked!"

# Please note, although callbacks are supported, you have to remember that values are saved only after the user clicked "Apply". The user might still click on cancel.
def otherCallbacks(objName, value):
    print "The object", objName, "was used, new value is", value

# Set default values here
defset = {
            "FlashSettingsFile" : "json",
            "checkBoxA" : True
            
            
            
    }

# Some layout data
layout = {
        "height" : layoutHeight,
        "homeUrl" : modpackUrl,
        "updateUrl" : "http://pastebin.com/raw.php?i=8V8SaUXC",
        "version" : installedVersion,
        "callback" : "Webium_applyButton",
        "items" : {
            "notice" : {
                "type" : "textfield",
                "x" : 23,
                "y" : 25,
                "label" : "information",
                },
            "notice1" : {
                "type" : "textfield",
                "x" : 23,
                "y" : 50,
                "width" : 240,
                "label" : "changelog"
                },
            "info" : {
                "type" : "textfield",
                "x" : 380,
                "y" : 50,
                "width" : 240,
                "label" : "info"
                },
            
            }
    }

#You can either specify the language strings hardcoded here, or simply load a json file with the same structure.
language = {
    "en" : {
        "information": "Webium's modpack Installer.",
        "changelog" : changelogXml,        
        "info" : infoXml
        },
    "cs" : {
        "information": "Webium modpack Installer.",        
        "changelog" : changelogXmlCs,        
        "info" : infoXmlCs
        },
    }

try:
    ms = ModSettingsAPI("Webium's modpack", "webium", defset, layout, language)
    ms.registerFunction("Webium_applyButton", applyButtonPressed)
    ms.registerFunction("Webium_button", buttonPressed)
    ms.registerFunction("Webium_otherCallbacks", otherCallbacks)
except Exception, err:
    print "[WebiumMod] exception",err

#old webium version checker part 2
from gui import SystemMessages
sys_msg = ''

def info():
    try:
        if len(sys_msg) != 0:
            if SystemMessages.g_instance is None:
                BigWorld.callback(4.0, info)
            else:
                if installedVersion == latestVersion:
                    SystemMessages.pushMessage(sys_msg)
                else:
                    SystemMessages.pushMessage(sys_msg, type=SystemMessages.SM_TYPE.Warning)
                    
    except:
        LOG_CURRENT_EXCEPTION()

    return


if installedVersion == latestVersion:
    sys_msg = '<font color="#7FCF00">Webium\'s modpack v.' + installedVersion +'&nbsp;'+ upToDate + '</font>' 
    #LOG_NOTE(upToDate + installedVersion)    
else:
    sys_msg = '<font color="#FF0000">Webium\'s modpack v.' + installedVersion + '</font>\n<font color="#FFED2F">v.'+ latestVersion +'&nbsp;'+ updateAvailable +'</font>\n' 
    #LOG_NOTE(updateAvailable + latestVersion)    
BigWorld.flushPythonLog()
BigWorld.callback(6.0, info)
print installedVersion, latestVersion
#end of old version checker
