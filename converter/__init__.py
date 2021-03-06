import subprocess
import os
import config
from platform import system

vp9_presets = {
    'ultrafast': ['-quality', 'realtime', '-speed', '8', '-tile-columns', '2', '-row-mt', '1'],
    'superfast': ['-quality', 'realtime', '-speed', '8', '-tile-columns', '2', '-row-mt', '1'],
    'veryfast': ['-quality', 'realtime', '-speed', '7', '-tile-columns', '2', '-row-mt', '1'],
    'faster': ['-quality', 'realtime', '-speed', '6', '-tile-columns', '2', '-row-mt', '1'],
    'fast': ['-quality', 'realtime', '-speed', '5', '-tile-columns', '2', '-row-mt', '1'],
    'medium': ['-quality', 'good', '-speed', '4', '-tile-columns', '2', '-row-mt', '1'],
    'slow': ['-quality', 'good', '-speed', '2', '-tile-columns', '2', '-row-mt', '1'],
    'slower': ['-quality', 'good', '-speed', '1', '-tile-columns', '2', '-row-mt', '1'],
    'veryslow': ['-quality', 'good', '-speed', '0', '-tile-columns', '2', '-row-mt', '1'],
    'placebo': ['-quality', 'best', '-speed', '0', '-tile-columns', '2', '-row-mt', '1']
}

def convert(vcodec:str, sources_list:list, mode:int, crf:int, bitrate:int, preset:str, callback, convert_done_callback):
    if mode==0:
        callback(len(sources_list))
    elif mode==1:
        callback(len(sources_list)*2)
    for source in sources_list:
        passn = mode+1
        for p in range(passn):
            commandline = []
            if config.ffmpeg_path is not None:
                commandline += [config.ffmpeg_path]
            else:
                commandline += ['ffmpeg']
            commandline += ['-i', source,]
            if not (mode==1 and p==0):
                commandline += ['-map', '0:v:0', '-map', '0:a:0']
            else:
                commandline += ['-map', '0:v:0']

            if vcodec == 'libx264':
                commandline += ['-vcodec', vcodec, '-preset', preset, '-profile:v', 'high', '-level', '4.1']
            elif vcodec == 'libx265':
                commandline += ['-vcodec', vcodec, '-preset', preset, '-profile:v', 'main']
            elif vcodec == 'libvpx-vp9':
                commandline += ['-vcodec', vcodec]
                commandline += vp9_presets[preset]

            if mode==0:
                commandline += ['-b:v', '0','-crf', str(crf)]
            elif mode==1:
                commandline += ['-b:v', str(bitrate)+'k']
                if vcodec == 'libx264' or vcodec == 'libvpx-vp9':
                    commandline += ['-pass', str(p+1)]
                elif vcodec == 'libx265':
                    commandline += ['-x265-params', 'pass={}'.format(p+1)]
            if (mode == 1 and p == 0):
                if vcodec == 'libvpx-vp9':
                    commandline += [os.path.splitext(source)[0]+'_out.mkv']
                else:
                    commandline += ['-f', 'null']
                    if system()=='Windows':
                        commandline+=['NUL']
                    else:
                        commandline+=['/dev/null']
            else:
                commandline+=['-acodec', 'copy', '-y', os.path.splitext(source)[0]+'_out.mkv']
            print(commandline)
            subprocess.run(commandline)
            callback()
    convert_done_callback()
