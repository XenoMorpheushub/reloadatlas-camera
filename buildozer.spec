[app]

title = ReloadAtlas Camera
package.name = reloadatlascamera
package.domain = org.reloadatlas

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0

requirements = python3==3.11.9,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = CAMERA,INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE

log_level = 2

android.archs = arm64-v8a,armeabi-v7a

android.api = 33
android.minapi = 24
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
