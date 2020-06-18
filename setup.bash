cp -r /home/recognition/SignalRecognition/install/icon /home/recognition/
echo "* * * * * recognition bash /home/recognition/SignalRecognition/install/arrancar.bash" > /etc/cron.d/arrancar_recognition
echo "* * * * * recognition bash /home/recognition/SignalRecognition/install/limpiar.bash" > /etc/cron.d/limpiar_recognition
