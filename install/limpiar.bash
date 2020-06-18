array=($(ls -tr /home/recognition/images/))
echo "${#array[@]}"

if ((${#array[@]} > 12000))
then
	for (( i=0; i<4000; i++))
	do
		rm "/home/recognition/images/${array[$i]}"
	done
fi
