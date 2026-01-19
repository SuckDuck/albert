xset s off
xset s noblank
xset -dpms
systemd-inhibit --what=sleep:idle:handle-lid-switch --who=kiosk --why="No sleep" sleep infinity &
dwm &
sleep 10
exec python /home/albert/albert/albert.py