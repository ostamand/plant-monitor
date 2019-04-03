


Connect to REPL using `screen`.

```
screen /dev/tty.SLAB_USBtoUART 115200
```

`CTRL+A` then `CTRL+D` to disconnect.

To send a file using ampy.

```
ampy --port /dev/tty.SLAB_USBtoUART put test.py
```

To run a file using ampy.

```
ampy --port /dev/tty.SLAB_USBtoUART run --no-output main.py
```
