xset s off
xset s noblank
xset -dpms
systemd-inhibit --what=sleep:idle:handle-lid-switch --who=kiosk --why="No sleep" sleep infinity &
dwm &
exec firefox mazcr.com