# cliphelp


Since qemu doesn't have an integrated clipboard sharing between guest and host when using
the built-in UI (gtk or sdl).

I've created a simple script for sharing clipboard between qemu guest and host machine through
a shared file between host and guest.

it works by constantly monitoring the shared file between host and the guest
if the file changes the contents will be then saved to the clipboard



EXECUTION:
run this on both guest and host

./cliphelp -f "PATH/OF/THE/SHARED/CLIPBOARDFILE"
