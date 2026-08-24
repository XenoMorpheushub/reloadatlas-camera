[app]

title = ReloadAtlas Camera
package.name = reloadatlascamera
package.domain = org.reloadatlas

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0

requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

# Camera + reseaux + Bluetooth (classique et Android 12+).
android.permissions = CAMERA,INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE

#
# Build configuration
#

log_level = 2

android.archs = arm64-v8a,armeabi-v7a

# Android moderne ; minapi 24 = Android 7.0, largement suffisant.
android.api = 33
android.minapi = 24

# Accepte automatiquement les licences du SDK Android (indispensable en CI).
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
