#!/bin/sh

gstinspect="/usr/bin/gst-inspect"

if [ ! -x $gstinspect ]; then
	cat > /dev/null
	exit 0
fi

case $1 in
-P|--provides)
	while read filename; do
	case "$filename" in
	*.so)
		$gstinspect --print-plugin-auto-install-info --rpm "$filename" 2> /dev/null | while read line; do
			echo -n "$line"
			
			if file $filename 2> /dev/null | grep "ELF 64-bit" >/dev/null ; then
				echo -n "()(64bit)"
			fi
			
			echo
		done
		;;
	esac
	done
	;;
esac

exit 0
