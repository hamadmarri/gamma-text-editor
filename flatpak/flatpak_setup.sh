#! /usr/bin/bash

# copy icon to ~/.icons
install -d /app/share/icons/hicolor/128x128/apps/
install -d /app/share/icons/hicolor/64x64/apps/
install -D ./bin/icon.svg /app/share/icons/hicolor/128x128/apps/io.gitlab.hamadmarri.gamma.svg
install -D ./bin/icon.svg /app/share/icons/hicolor/64x64/apps/io.gitlab.hamadmarri.gamma.svg


# edit io.gitlab.hamadmarri.gamma.desktop put the path 
cp ./bin/io.gitlab.hamadmarri.gamma.desktop.bak ./bin/io.gitlab.hamadmarri.gamma.desktop
sed -i -e "s,\[gamma path placeholder\], /app/bin/gamma," ./bin/io.gitlab.hamadmarri.gamma.desktop

# and copy to ~/.local/share/applications
install -d /app/share/applications/
install -D ./bin/io.gitlab.hamadmarri.gamma.desktop /app/share/applications/



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





