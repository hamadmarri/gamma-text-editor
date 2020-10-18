#!/usr/bin/env bash


# Expected arguments:
# $1 :  The directory where gamma.py is installed
# $2 :  Whether to copy config.py also.
#       -> config.py will be copied to user's
#          .config directory if $2 equals 1


# It is assumed that home_dir_data folder is
# residing along with gamma.py directory and the below
# folders/files were moved there while packaging:
#       config.py
#       signal_handler.py
#       plugins/
#       style/
#       ui


# Packager should set package_date to the unix timestamp when packaging.
# Use shell command 'date +%s' to get timestamp.
package_date=0000000000


# Create relevant directory structure if it doesn't exist
mkdir -p /home/$USER/.config/gamma-text-editor/.backup/

# Create a backup of old data
cp /home/$USER/.config/gamma-text-editor/* /home/$USER/.config/gamma-text-editor/.backup/ -r 2>/dev/null

# Copy files from install directory to .config directory.
# config.py is left out here and will be copied later.
cp $1/home_dir_data/{signal_handler.py,plugins,style,ui} /home/$USER/.config/gamma-text-editor/ -r

if [ $2 == "1" ]
then
    cp $1/home_dir_data/config.py /home/$USER/.config/gamma-text-editor/
fi

chmod 755 -R /home/$USER/.config/gamma-text-editor/

# Write the timestamp to .config foler for future reference
echo $package_date > /home/$USER/.config/gamma-text-editor/package_date

echo "Inititalized config at /home/$USER/.config/gamma-text-editor/"