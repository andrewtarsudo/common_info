# Bash Commands

`man <command>`<br/>
manual, вывести мануал на экран<br>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# man mkdir
MKDIR(1)                         User Commands                        MKDIR(1)

NAME
       mkdir - make directories

SYNOPSIS
       mkdir [OPTION]... DIRECTORY...

DESCRIPTION
       Create the DIRECTORY(ies), if they do not already exist.

       Mandatory  arguments  to  long  options are mandatory for short options too.

       -m, --mode=MODE
              set file mode (as in chmod), not a=rwx - umask

       -p, --parents
              no error if existing, make parent directories as needed

       -v, --verbose
              print a message for each created directory

 Manual page mkdir(1) line 1 (press h for help or q to quit)
```
  </p>
</details>
<br/>

`pwd` <br/>
print working directory, вывод полного пути до текущей директории<br/>
<details>
  <summary>Пример</summary>
  <p>
    
```
zbash# pwd
/Users/user
```
  </p>
</details>
<br/>

`ls`  <br/>
list the content, отобразить содержимое директории<br/>
<details>
  <summary>Пример</summary>
  <p>
```
zbash# ls
.localized	Shared		user
```
  </p>
</details>
<br/>

`ls -a`<br/>
list all files, отобразить все содержимое директории, включая скрытые файлы<br>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# ls -a
.		..		.localized	Shared		user
```
  </p>
</details>
<br/>

`ls -l`<br/>
list files in detail, отобразить подробную информацию о содержимом директории<br>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# ls -l
total 0
-rw-r--r--   1 root           wheel     0 Jan  1  2020 .localized
drwxrwxrwt   9 root           wheel   288 Jan  1  2020 Shared
drwxr-xr-x+ 42 AndrewTarasov  staff  1344 May  2 21:44 user
```
  </p>
</details>
<br/>

`cd <path>`<br/>
change directory, перейти в другую директорию<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cd Applications/Mattermost.app
```
  </p>
</details>
<br>

`cd ..`<br/>
change directory to the parent one, перейти в директорию на уровень выше, в родительскую
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cd ..
/Applications
```
  </p>
</details>
<br/>

`cd /`<br/>
change the directory to the root, перейти в корневую директорию
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cd /
```
</p>
</details>
<br/>

`cd ~`<br/>
change the directory to the home, перейти в директорию, которая задана как домашняя
<details>
  <summary>Пример</summary>
  <p>

  ```
zbash# cd ~
```
  </p>
</details>
<br/>

> Примечание.
> Допускается комбинировать "..", "~", "/" и названия директорий.

`mkdir <dirName>`<br/>
make a directory, создать директорию<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# mkdir NewFolder
```
  </p>
</details>
<br/>

`mkdir -p <dirName>`<br/>
make a directory of that path, создать директорию по этому пути, создавая не существующие директории<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# mkdir -p ./NewFolder2/NewFolder
```

  </p>
</details>
<br/>

`mv <file> <newPlace>`<br/>
move the file, переместить файл<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# mv NewFolder ./Chemistry
```
  </p>
</details>
<br/>

`mv <file> <newName>`<br/>
rename the file, переименовать файл<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# mv NewFolder newName
```
  </p>
</details>
<br/>

`cp <file> <path>`<br/>
copy the file, копировать файл<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cp NewFolder Chemistry
```
  </p>
</details>
<br/>

`rm <file>`<br/>
remove the item, удалить элемент
<details>
  <summary>Пример</summary>
  <p>

```
zbash# rm text_file.txt
```
</p>
</details>
<br/>

`rm -i <file>`<br/>
remove with the Information table, удалить элемент с подтверждением
<details>
  <summary>Пример</summary>
  <p>

```
zbash# rm -i text_file.txt
remove text_file.txt? y
```
  </p>
</details>
<br/>

`rmdir <emptyDir>`<br/>
remove the empty directory, удалить пустую директорию
<details>
  <summary>Пример</summary>
  <p>

```
zbash# rmdir NewFolder2
```
  </p>
</details>
<br/>

`rm -rf <dirName>`<br/>
ReMove any DIRectory using the command Recursively and Forcing, удалить директорию, применяя команду принудительно и рекурсивно к файлам внутри папки<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# rm -rf NewFolder
```
  </p>
</details>
<br/>

`apt-get <command>`<br/>
Application Package Tool, программа для работы с пакетами приложений<br/>

`apt-get install <package>`<br/>
install the application, установить пакет<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# apt-get install wget
```
  </p>
</details>
<br/>

`apt-get search <package>`<br/>
search the application, найти пакет<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# apt-get search wget
```
  </p>
</details>
<br/>

`!!`<br/>
repeat the last command, повторить последнюю команду<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cd ..
zbash# !!
cd ..
```
  </p>
</details>
<br/>

> Примечание.
> Допускается комбинировать с другими командами.

<details>
  <summary>Пример</summary>
  <p>

```
zbash# cd ..
zbash# !!/Users
cd ../Users
```
  </p>
</details>
<br/>

`ps`<br/>
show current user processes, показать все процессы пользователя<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# ps
PID  TTY        TIME    CMD
2468 ttys000    0:00.22 -zsh
8390 ttys000    0:00.15 /Library/Developer/CommandLineTools/usr/bin/git -C /us
8391 ttys000    0:14.15 /Library/Developer/CommandLineTools/usr/libexec/git-co
8452 ttys000    0:28.52 /Library/Developer/CommandLineTools/usr/libexec/git-co
8407 ttys001    0:00.14 -zsh
```
  </p>
</details>
<br/>

`kill <PID>` / `kill -15 <PID>`<br/>
kill the process with TERM, убить процесс с помощью принудительного завершения задачи<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# kill 8525
zbash# kill -15 8526 8527
```
  </p>
</details>
<br/>

`kill -9 <PID>`<br/>
kill the process with SIGKILL, убить процесс сигналом SIGKILL, который имеет наивысший приоритет<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# kill -9 8528
```
  </p>
</details>
<br/>

`sudo <command>`<br/>
become a super user for one command, запустить команду от имени суперпользователя, вводится пароль учетной записи, под которой зашли в систему<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# sudo su
Password:
```
  </p>
</details>
<br/>

`su`<br/>
switch to the superuser, войти в систему как суперпользователь, вводится пароль от учетной записи суперпользователя<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# su
Password:
```
  </p>
</details>
<br/>

`exit`<br/>
leave any shell, выйти из любой оболочки<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# ssh support@192.168.99.101
[support@99.101] exit
zbash#
```
  </p>
</details>
<br/>

`clear`<br/>
move the terminal to the top, переместить строку терминала на самый верх<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# clear
```
  </p>
</details>
<br/>

`<command> -h` / `<command> --help`<br/>
help information for the command, вывести справочную информацию<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# man --help
man, version 1.6g

usage: man [-adfhktwW] [section] [-M path] [-P pager] [-S list]
	[-m system] [-p string] name ...

  a : find all matching entries
  c : do not use cat file
  d : print gobs of debugging information
  D : as for -d, but also display the pages
  f : same as whatis(1)
  h : print this help message
  k : same as apropos(1)
  K : search for a string in all pages
  t : use troff to format pages for printing
  w : print location of man page(s) that would be displayed
      (if no name given: print directories that would be searched)
  W : as for -w, but display filenames only

  C file   : use `file' as configuration file
  M path   : set search path for manual pages to `path'
  P pager  : use program `pager' to display pages
  S list   : colon separated section list
  m system : search for alternate system's man pages
  p string : string tells which preprocessors to run
               e - [n]eqn(1)   p - pic(1)    t - tbl(1)
               g - grap(1)     r - refer(1)  v - vgrind(1)
```
  </p>
</details>
<br/>

`cat <file>`<br/>
concatenate the list of files, вывести содержимое нескольких файлов на одном экране<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# cat TextFile.txt TextFile2.txt
Text 1 Line 1
Text 1 Line N
Text 2 Line 1
Text 2 Line M
```
  </p>
</details>
<br/>

`less <textfile>`<br/>
show text file, отобразить содержимое текстового файла<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# less TextFile.txt
Text 1 Line 1
Text 1 Line N
```
  </p>
</details>
<br/>

`nano`<br/>
minimalistic command-line text editor, минималистичный GUI-текстовый редактор в командной строке<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# nano
GNU nano 2.0.6                New Buffer

^G Get Help  ^O WriteOut  ^R Read File ^Y Prev Page ^K Cut Text  ^C Cur Pos
^X Exit      ^J Justify   ^W Where Is  ^V Next Page ^U UnCut Text^T To Spell
```
  </p>
</details>
<br/>

`top`<br/>
the information about the processes, вывод информации о текущих процессах и состоянии системы<br/>
<details>
  <summary>Пример</summary>
  <p>

```Processes: 264 total, 7 running, 4 stuck, 253 sleeping, 1883 threads   22:24:02
Load Avg: 2.93, 3.28, 3.74  CPU usage: 57.7% user, 10.27% sys, 32.64% idle
SharedLibs: 199M resident, 51M data, 14M linkedit.
MemRegions: 317181 total, 4194M resident, 35M private, 364M shared.
PhysMem: 8042M used (2667M wired), 149M unused.
VM: 1425G vsize, 2305M framework vsize, 537950136(4960) swapins, 542685115(16345
Networks: packets: 105734371/137G in, 29520336/3566M out.
Disks: 126839932/2682G read, 42074223/2487G written.

PID    COMMAND      %CPU  TIME     #TH   #WQ  #PORTS  MEM    PURG  CMPRS  PGRP
1513   Atom Helper  209.9 05:27:26 23/4  1    192     3249M- 0B    236M-  1468
0      kernel_task  17.0  31:26:32 176/4 0    0       612M-  0B    0B     0
135    WindowServer 11.8  125 hrs  13    6    2913-   349M+  152K- 115M-  135
2461   Terminal     9.2   01:47.76 9     3    502-    34M-   868K+ 17M-   2461
10076  top          7.9   00:01.38 1/1   0    26      7528K  0B    0B     10076
9761   gamecontroll 1.3   00:09.88 5/2   4/1  67      1460K+ 0B    532K   9761
2408   plugin-conta 0.8   06:08:46 30    1    3399    787M   0B    741M-  2391
1468   Atom         0.8   06:24:02 34    2    416     116M+  0B    59M    1468
1472   ControlCente 0.7   09:33.92 5     2    560+    39M-   0B    28M-   1472
1588   firefox      0.5   87:15:06 93    5    131476+ 1795M+ 0B    1586M- 1588
74     powerd       0.5   10:27.91 4     3    127+    2540K+ 0B    992K-  74
2391   Ghostery     0.3   51:55:36 86    5    754+    1027M+ 0B    853M-  2391
2404   plugin-conta 0.3   04:12:24 33    1    1324    377M   0B    362M   2391
2400   plugin-conta 0.3   05:08:39 30    1    2189    999M   0B    937M-  2391
61     UserEventAge 0.3   11:24.74 6     3    701+    2972K+ 0B    1596K- 61
522    corespotligh 0.3   00:39.11 7     5    131+    6404K+ 0B    5500K- 522
```
  </p>
</details>
<br/>

`sh <pathScript>`<br/>
execute the shell script, выполнить скрипт оболочки<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# sh /usr/local/Homebrew/Library/Homebrew/brew.sh
```
  </p>
</details>
<br/>

`locate <file>`<br/>
cached list of searching files, fast and outdated, поиск файла по сохраненной базе файлов, быстро, но не отображает последние изменения<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# locate temp
/Users/user/Desktop/temp
```
  </p>
</details>
<br/>

`locate -i <file>`<br/>
cached list of searching files, fast and outdated and ignore the case, поиск файла по сохраненной базе файлов без учета регистра, быстро, но не отображает последние изменения<br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# locate -i temp
/Users/user/Desktop/temp
/Users/user/Desktop/Template_guide.dotm
```
  </p>
</details>
<br/>

`find <path> -name "<fileName>"`<br/>
finds actual files, slow and up-to-date, <br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# find /Users/user/Desktop -iname "temp*"
/Users/user/Desktop/temp
/Users/user/Desktop/Template_guide.dotm
/Users/user/Desktop/Work/Templates
```
  </p>
</details>
<br/>

`find <path> -iname "<fileName>"`<br/>
finds actual files, slow and up-to-date and ignore case, <br/>
<details>
  <summary>Пример</summary>
  <p>

```
zbash# find /Users/user/Desktop -iname "temp*"
/Users/user/Desktop/temp
/Users/user/Desktop/Template_guide.dotm
/Users/user/Desktop/Work/Templates
```
  </p>
</details>
<br/>

`wget <URL>`<br/>
download the file, загрузить файл<br/>
<details>
  <summary>Пример</summary>
  <p>

```
wget http://example.com/example.png
```
  </p>
</details>
<br/>

`wget -r <URL>`<br/>
download the file recursively, загрузить файл рекурсивно<br/>
<details>
  <summary>Пример</summary>
  <p>

```
wget -r http://example.com/example/
```
  </p>
</details>
<br/>

`grep '<pattern>' <file>`<br/>
search Globally for regular expressions and patterns, глобальный поиск по содержимому с помощью регулярных выражений и масок<br/>
<details>
  <summary>Пример</summary>
  <p>

```
grep 'Line \*' /Users/user/Desktop/TextFile.txt
```
  </p>
</details>
<br/>

`grep -i '<pattern>' <file>` / `grep --ignore-case '<pattern>' <file>`<br/>
поиск без учета регистра, по умолчанию регистрозависимый<br/>
`grep -H '<pattern>' <file>`<br/>
выводить название файла вместе с найденными строками<br/>
`grep -h '<pattern>' <file>` / `grep --no-filename '<pattern>' <file>`<br/>
не выводить названия файлов, где надены подходящие строки<br/>
`grep -a '<pattern>' <file>` / `grep --text '<pattern>' <file>`<br/>
рассматривать все файлы как ASCII, в том числе и бинарные<br/>
`grep -n '<pattern>' <file>` / `grep --line-number '<pattern>' <file>`<br/>
указать номер строки, где встречается искомое выражение, для каждого файла, начиная с 1, строки каждого файла нумеруются отдельно<br/>
`grep --null '<pattern>' <file>`<br/>
напечатать \0 после названия файла<br/>
`grep -R '<pattern>' <file>` / `grep -r '<pattern>' <file>` /
`grep --recursive '<pattern>' <file>`<br/>
искать рекурсивно по всем поддиректориям<br/>
`grep -v '<pattern>' <file>` / `grep --invert-match '<pattern>' <file>`<br/>
вывести строки, в которых отсутствует указанное выражение<br/>
