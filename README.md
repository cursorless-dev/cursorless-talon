# Cursorless talon

This repository contains the talon side of [Cursorless](https://marketplace.visualstudio.com/items?itemName=pokey.cursorless).  

## Installation
First, install the dependencies:

### Dependencies
1. Install [Talon](https://talonvoice.com/)
2. Install [knausj_talon](https://github.com/knausj85/knausj_talon). Note that
   even a heavily modified version of knausj should be fine, but make sure you
   at least have [this
   commit](https://github.com/knausj85/knausj_talon/commit/ffe1fe0f6a5ffa594d31501dad3f4f4ae7751e62)
   (which is in mainline knausj).
3. Install [VSCode](https://code.visualstudio.com/)
4. Install the [VSCode talon extension pack](https://marketplace.visualstudio.com/items?itemName=pokey.talon)
5. Install the [Cursorless VSCode extension](https://marketplace.visualstudio.com/items?itemName=pokey.cursorless)

### Installing this repo
#### Linux & Mac

Clone repo into `~/.talon/user`

```insert code:
cd ~/.talon/user
git clone https://github.com/pokey/cursorless-talon cursorless-talon
```
    
Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.

The folder structure should look something like the below:

```insert code:
~/.talon/user/knausj_talon
~/.talon/user/knausj_talon/apps
~/.talon/user/knausj_talon/code
...
~/.talon/user/cursorless-talon
~/.talon/user/cursorless-talon/src
...
```

#### Windows

Clone repo into `%AppData%\Talon\user` 

```insert code:
cd %AppData%\Talon\user
git clone https://github.com/pokey/cursorless-talon cursorless-talon
```
    
Alternatively, access the directory by right clicking the Talon icon in taskbar, clicking Scripting>Open ~/talon, and navigating to user.
    
The folder structure should look something like the below:

```insert code:
%AppData%\Talon\user\knausj_talon
%AppData%\Talon\user\knausj_talon\apps
%AppData%\Talon\user\knausj_talon\code
...
%AppData%\Talon\user\cursorless-talon
%AppData%\Talon\user\cursorless-talon\src
...
```