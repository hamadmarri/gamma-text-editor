#!/usr/bin/env bash

# copy icon to ~/.icons
mkdir -p ~/.icons/ && cp ./bin/icon.svg ~/.icons/io.gitlab.hamadmarri.gamma.svg
mkdir -p ~/.local/share/icons/ && cp ./bin/icon.svg ~/.local/share/icons/io.gitlab.hamadmarri.gamma.svg


# edit io.gitlab.hamadmarri.gamma.desktop put the path 
cp ./bin/io.gitlab.hamadmarri.gamma.desktop.bak ./bin/io.gitlab.hamadmarri.gamma.desktop
sed -i -e "s,\[gamma path placeholder\],$PWD/bin/gamma," ./bin/io.gitlab.hamadmarri.gamma.desktop

# and move to ~/.local/share/applications
mkdir -p ~/.local/share/applications/ && mv ./bin/io.gitlab.hamadmarri.gamma.desktop ~/.local/share/applications/
 
 
# copy gtksource styles
mkdir -p ~/.local/share/gtksourceview-4/styles/ && cp ./gtksourceview_styles/* ~/.local/share/gtksourceview-4/styles/
 
 
 # create a symbolic link to gamma sh file
sudo ln -s $PWD/bin/gamma /usr/bin/gamma-editor

