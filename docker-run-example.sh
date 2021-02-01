# This is an example of how to run the Docker espresso-run image

docker run --detach --mount type=bind,source=/home/earl/PycharmProjects/espresso/.env,target=/espresso/.env,readonly --cap-drop SETGID --cap-drop SETUID --memory=1g --memory-swap=1g --cpus=1 --pids-limit 256 -p 5055:5000 espresso-run

