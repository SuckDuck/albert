xset s noblank
xset -dpms
systemd-inhibit --what=sleep:idle:handle-lid-switch --who=kiosk --why="No sleep" sleep infinity &

dwm &
feh --bg-fill /home/albert/albert/wp.png
keepalive --active --duration 87600h &

until ping -c1 -W1 1.1.1.1 >/dev/null 2>&1; do
  sleep 1
done

while true; do
  python /home/albert/albert/albert.py
  sleep 2
done