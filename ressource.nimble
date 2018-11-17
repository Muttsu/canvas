let backend = "ressource"
let frontend = "index"

let backendpath = "src/" & $backend
let frontendpath = "src/" & $frontend


# Package

version       = "0.1.0"
author        = "Muttsu"
description   = "canvas backend ressources"
license       = "MIT"
srcDir        = "src"
bin           = @[$backend]
skipExt       = @["nim"]


# Dependencies

requires "nim >= 0.19.0"
requires "jester 0.4.1"
requires "karax 0.2.0"


# Tasks

task mount, "Run the ressource service":
    exec "nim c " & $backendpath
    mkDir "bin/"
    rmFile "bin/" & $backend .toExe
    mvFile $backendpath.toExe, "bin/" & $backend .toExe
    exec "bin/" & $backend .toExe

task compile, "Compile the ressource service":
    exec "nim c " & $backendpath
    mkDir "bin/"
    rmFile "bin/" & $backend .toExe
    mvFile $backendpath.toExe, "bin/" & $backend .toExe

task start, "Runs the ressource service":
    if not fileExists "bin/" & $backend .toExe:
        exec "nim c " & $backendpath
        mkDir "bin/"
        rmFile "bin/" & $backend .toExe
        mvFile $backendpath.toExe, "bin/" & $backend .toExe
    exec "bin/" & $backend .toExe
