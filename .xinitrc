xset s noblank
xset -dpms
systemd-inhibit --what=sleep:idle:handle-lid-switch --who=kiosk --why="No sleep" sleep infinity &

dwm &
unclutter --timeout 0 --start-hidden --jitter 5 &

feh --bg-fill /home/albert/albert/wp.png

until ping -c1 -W1 1.1.1.1 >/dev/null 2>&1; do
  sleep 1
done

while true; do
  python /home/albert/albert/albert.py
  sleep 2
done