[app]

# App info
title = DDL任务规划器
package.name = ddlplanner
package.domain = org.ddl.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf
source.exclude_dirs = tests, __pycache__, .git
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Android
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.private_storage = True
android.permissions = INTERNET
android.accept_sdk_license = True
android.archs = arm64-v8a
android.add_src =
android.gradle_dependencies =

[buildozer]
log_level = 2
warn_on_root = 1
