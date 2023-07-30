echo "Test: /dev differnces"
ls -al /dev > ~/log1
echo "Plug/unplug the device in 5 sec"
sleep 5
ls -al /dev > ~/log2
diff ~/log1 ~/log2