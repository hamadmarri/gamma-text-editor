#! /usr/bin/bash

# copy icon to ~/.icons
mkdir -p ~/.icons/ && cp ./bin/icon.svg ~/.icons/com.github.hamadmarri.gamma.svg


# edit com.github.hamadmarri.gamma.desktop put the path 
cp ./bin/com.github.hamadmarri.gamma.desktop.bak ./bin/com.github.hamadmarri.gamma.desktop
sed -i -e "s,\[gamma path placeholder\],$PWD/bin/gamma," ./bin/com.github.hamadmarri.gamma.desktop

# and copy to ~/.local/share/applications
mkdir -p ~/.local/share/applications/ && cp ./bin/com.github.hamadmarri.gamma.desktop ~/.local/share/applications/
 
 
# copy gtksource styles
mkdir -p ~/.local/share/gtksourceview-4/styles/ && cp ./gtksourceview_styles/* ~/.local/share/gtksourceview-4/styles/
 
 
 # create a symbolic link to gamma sh file
sudo ln -s $PWD/bin/gamma /usr/bin/gamma-editor

