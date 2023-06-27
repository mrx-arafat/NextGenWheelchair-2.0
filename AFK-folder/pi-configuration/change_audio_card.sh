#!/bin/bash

# Step 1: Execute 'arecord -l' and find the card number for "Device [USB Audio Device]"
output=$(arecord -l)
card_number=$(echo "$output" | grep -oP "(?<=card )\d+(?=:.*\[USB Audio Device\])")

# Step 2: Assign the card number to variable X
X=$card_number

# Step 3: Modify /usr/share/alsa/alsa.conf
sudo sed -i "s/defaults\.ctl\.card $CARD_NUMBER/defaults\.ctl\.card $X/" /usr/share/alsa/alsa.conf
sudo sed -i "s/defaults\.pcm\.card $CARD_NUMBER/defaults\.pcm\.card $X/" /usr/share/alsa/alsa.conf

# Step 5: Print the assigned card number
echo "Assigned card number: $X"

# Step 6: Ask user for a reboot
read -p "Do you want to reboot? (y/n) " choice
if [[ $choice == "y" || $choice == "Y" ]]; then
  # Step 7: Reboot as root
  sudo reboot
else
  # Step 7: Exit the program
  exit 0
fi
