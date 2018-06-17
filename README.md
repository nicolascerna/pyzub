## Pyzub: Manipulate subtitles

Pyzub is a small package and CLI for manipulating subtitles

**Suported Formats:**

- SubRip [.srt].

**Plans to Support:**

- SubStation Alpha [.ssa]
- SubViewer [.sub]
- Universal Subtitle Format [.usf]

### Installation:

Run `pip install pyzub`

### Command Line Interface:

At the moment only the *slide* command is available (arguably the most important feature).
The *slide* command of *pyzub* lets you move your subtitles so you can synchronize them manually.
	
```
$ pyzub slide -h
Usage: pyzub slide [OPTIONS] FILEPATH

Options:
  --hours FLOAT
  --minutes FLOAT
  --seconds FLOAT
  --milliseconds FLOAT
  --microseconds FLOAT
  --overwrite           Modifies the subtitle file in place.
  --verbose             Displays a progress bar and a message when finished.
  --help, -h            Show this message and exit.
```

**Example:**

This will move your subtitles by 2.5 seconds (you can also give negative values):

```bash
$ pyzub slide Game_of_Thrones_s03ep09.srt --seconds 2 --milliseconds 500
```

By default *pyzub* will generate an output file named *Game_of_Thrones_s03ep09_MODIFIED.srt*, unless ```--overwrite``` is used. The output file will always be in *utf-8* encoding and use your system new line character.

This is OK too:

```bash
$ pyzub slide Game_of_Thrones_s03ep09.srt --seconds -70.5 --milliseconds 5000
```
 This would move your subtitles 65.5 seconds back ~~in time~~.
 
### Package:

You can read a subtitle file:

```python
from pyzub.subfiles import SRTFile

filepath = '/home/user/mysubtitle.srt'
subfile = SRTFile(filepath)
```

Iterate over the file:
```
for subtitle in subfile:
	print(subtitle)
```

Print a SRTFile:

```python
print(subfile)
```

```
Relative Path: /home/user/mysubtitle.srt
Codec: ISO-8859-1
No. of Subtitles: 451
```

Get a subtitle:

```python
# idx could be a number from 1 to 451 in this case
subtitle = subfile.get_subtitle(idx)
```

Print the subtitle:

```python
print(subtitle)
```

```
Index: 1
Start Time: 00:00:04,605
End Time: 00:00:06,105
Text: En un día cualquiera,
```

An of course modify anything you want directly:

```python
# modify the text
subtile.text = 'modified subtitle'

# times use timedelta from the datetime package
subtitle.start_time = timedelta(minutes=10)
# also, you can assign directly a string
subtitle.end_time = '01:25:59,650'

# write the changes to disk
subfile.dump('/home/user/mysubtitle_modified.srt')
```

And finally:

```
print(len(subfile))
# output: 451 (i.e, the number of subtitles in the file)
```

```
print(len(subtitle))
# output: 21 (i.e, the number of chars in the subtitle's text attribute)
```

### Planned features:
- Insert, delete subtitles, etc.
- Automatic grammar and syntax correction

### License

MIT

