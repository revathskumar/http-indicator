import os
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from subprocess import Popen, PIPE
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'HTTP Indicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icon.png'), appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    processes = get_process()
    if processes:
        for x in processes:
            if not x.strip():
                continue
            process_menu_item = gtk.MenuItem(x)
            menu.append(process_menu_item)
    else:
        empty_menu_item = gtk.MenuItem('No node|ruby|python')
        menu.append(empty_menu_item)
    menu.append(gtk.SeparatorMenuItem())
    quit_menu_item = gtk.MenuItem('Quit')
    quit_menu_item.connect('activate', quit)
    menu.append(quit_menu_item)
    menu.show_all()
    return menu

def get_process():
    p1 = Popen(['lsof', '-iTCP', '-sTCP:LISTEN', '-P'], stdout=PIPE)
    p2 = Popen(["grep", "-E", "node|ruby|python"], stdin=p1.stdout, stdout=PIPE)
    p3 = Popen(["awk", '{ print $1 " - " $2 " - " $9 }'], stdin=p2.stdout, stdout=PIPE)
    output = p3.communicate()[0]
    if output:
        return output.split("\n")

def quit(_):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

main()
