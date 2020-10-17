#!/usr/bin/env bash

mkdir -p /home/$USER/.config/gamma-text-editor/
cp $1/home_dir_data/* /home/$USER/.config/gamma-text-editor/ -r
chmod 755 -R /home/$USER/.config/gamma-text-editor/

echo "Inititalized config at /home/$USER/.config/gamma-text-editor/"