#!/bin/bash
# Sintetizza con ffmpeg i suoni che non sono nella libreria HyperFrames (nessun download, nessuna licenza).
# Uso: bash sfx8.sh "<progetto>/assets/sfx8"
set -e
OUT="${1:-assets/sfx8}"; mkdir -p "$OUT"; cd "$OUT"
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=pink:amplitude=0.6:d=0.38:seed=7" -af "highpass=f=1800,lowpass=f=6000,volume=1.6,afade=t=in:d=0.04,afade=t=out:st=0.22:d=0.16" tratto.mp3   # penna
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.35*sin(2*PI*(500*t+2600*t*t))*exp(-18*t)':d=0.18:s=44100" bolla.mp3                                                                    # bollicina
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.3*sin(2*PI*1400*t)*exp(-60*t)':d=0.05:s=44100" tick.mp3                                                                                 # tick
# 8-bit (scene pixel)
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.25*sgn(sin(2*PI*(if(lt(t,0.08),988,1319))*t))*exp(-3*max(0,t-0.08))':d=0.45:s=44100" coin.mp3
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.22*sgn(sin(2*PI*(300*t+1800*t*t)))*(1-t/0.3)':d=0.3:s=44100" jump.mp3
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.2*sgn(sin(2*PI*1760*t))*(1-t/0.07)':d=0.07:s=44100" blip.mp3
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.22*sgn(sin(2*PI*(if(lt(t,0.1),523,if(lt(t,0.2),659,if(lt(t,0.3),784,1047))))*t))*if(lt(t,0.4),1,exp(-6*(t-0.4)))':d=0.7:s=44100" powerup.mp3
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.22*sgn(sin(2*PI*(880-1200*t)*t))*(1-t/0.35)':d=0.35:s=44100" down.mp3
ls
