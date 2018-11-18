let backend = "resource"
let frontend = "index"

let backendpath = "src/" & $backend
let frontendpath = "src/" & $frontend


# Package

version       = "0.1.0"
author        = "Muttsu"
description   = "canvas backend resources"
license       = "MIT"
srcDir        = "src"
bin           = @[$backend]
skipExt       = @["nim"]


# Dependencies

requires "nim >= 0.19.0"
requires "jester 0.4.1"
requires "karax 0.2.0"
requires "jwt >= 0.0.1"


# Tasks

task mount, "Run the resource service":
    exec "nim c " & $backendpath
    exec $backend .toExe

task run, "Runs the resource service":
    exec $backend .toExe
