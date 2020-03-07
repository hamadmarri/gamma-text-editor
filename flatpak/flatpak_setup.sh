#! /usr/bin/bash

# copy icon to ~/.icons
install -d /app/share/icons/hicolor/128x128/apps/
install -d /app/share/icons/hicolor/64x64/apps/
install -D ./bin/icon.svg /app/share/icons/hicolor/128x128/apps/com.github.hamadmarri.gamma.svg
install -D ./bin/icon.svg /app/share/icons/hicolor/64x64/apps/com.github.hamadmarri.gamma.svg


# edit com.github.hamadmarri.gamma.desktop put the path 
cp ./bin/com.github.hamadmarri.gamma.desktop.bak ./bin/com.github.hamadmarri.gamma.desktop
sed -i -e "s,\[gamma path placeholder\], /app/bin/gamma," ./bin/com.github.hamadmarri.gamma.desktop

# and copy to ~/.local/share/applications
install -d /app/share/applications/
install -D ./bin/com.github.hamadmarri.gamma.desktop /app/share/applications/



# copy fonts
# install -d /app/share/fonts/
# cp -ar /usr/share/fonts/. /app/share/fonts




# copy dir to /app/
install -D ./bin/gamma /app/bin/gamma

install -D ./*.py /app/

cp -R ./plugins /app/

install -d /app/style/
install -D ./style/*.css /app/style/

install -d /app/ui/
install -D ./ui/* /app/ui/


install -D ./gtksourceview_styles/* /app/share/gtksourceview-4/styles





