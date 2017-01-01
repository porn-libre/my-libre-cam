#!/bin/bash
#
#   AGPL v3+
#

# kill qwebirc
kill $(ps ax | grep run.py | head -n1 | sed 's/^[ \t]*//g;'| cut -d" " -f1 > /dev/null) 2> /dev/null
killall vlc

PORTV=9091
PORTA=9092
CODE="#transcode{vcodec=MJPG,width=528,vb=1250,fps=5,venc=ffmpeg{strict=1},sfilter=logo}:standard{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=127.0.0.1:${PORTV}/cam.mjpg"

echo "tor"

tor -f torrc 2> /dev/null 1> /dev/null &

[ -f "qr.png" ] && LOGO="--sub-filter logo --logo-x 3 --logo-y 3 --logo-position 6 --logo-file qr.png"
# -input-repeat=10000
# --v4l2-hflip 1 -
echo "vlc"
# http://www.netinstructions.com/automating-picture-capture-using-webcams-on-linuxubuntu/
(vlc -d -vvv $LOGO v4l2:// --v4l2-fps 4 --no-audio --sout "$CODE" 2> /dev/null 1> /dev/null \
|| vlc -d -vvv $LOGO v4l:// --v4l-fps 4 --no-audio --sout "$CODE" 2> /dev/null 1> /dev/null \
|| exit 0) &

# microfono?
vlc -d -I dummy -vvv alsa://plughw --sout "#transcode{vcodec=none,acodec=vorb,ab=64,channels=1}:http{mux=ogg,dst=127.0.0.1:${PORTA}/audio.ogg}"  2> /dev/null 1> /dev/null &

# falta levantar el servidor para datos

while [ "$(cat broadcast/hostname 2> /dev/null)" == "" ]; do
    echo "moment please..."
    sleep 1
done

# alert
#torify 2> /dev/null wget http://mdj7ldtgoq22m3hi.onion/$(cat ~/.$PROG/broadcast/hostname)-${VERSION} -qO /dev/null

echo "irc"

# inicia el servidor IRC
ngircd -f ngircd.conf

sleep 6

rm -r ./compiled/ 2> /dev/null 1> /dev/null

# webcam in config.py
sed -i "s/^WEBCAM.*$/WEBCAM=\"http:\/\/$(cat broadcast/hostname):81\/cam.mjpg\"/g" config.py
sed -i "s/^AUDIO.*$/AUDIO=\"http:\/\/$(cat broadcast/hostname):82\/audio.ogg\"/g" config.py


echo "web"

./run.py 2> /dev/null 1> /dev/null

echo "URL: http://$(cat broadcast/hostname) open in torbrowser"
echo "private key: $(echo "$ADDRESS" | head -n1)"

[ ! "$(which qrencode)" == "" ] && grep "^BITCOIN" config.py | cut -d= -f2 | sed 's/[^0-9A-Za-z]//g; s/^/bitcoin:/g' | qrencode -o static/bitcoin.png
[ ! "$(which qrencode)" == "" ] && grep "^BITCOIN" config.py | cut -d= -f2 | sed 's/[^0-9A-Za-z]//g; s/^/bitcoin:/g' | qrencode -s 2 -o qr.png --background=FFFFFFAA

exit

TODO
====

* this script in python
* random mount point
* blog?
* irc over python
