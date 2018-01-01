The following Python packages are needed:
```
flask
json
rpy2 
```

Note `rpy2` was a little tricky.  To use with Python 2.7, you must install no later than v2.8.6.

```
pip install rpy==2.8.6
```

Also, on OSX, the default compiler doesn't work.  I had to compile use GCC7.
```
brew install gcc@7
brew ls gcc
export CC=/usr/local/Cellar/gcc/7.2.0/bin/x86_64-apple-darwin17.3.0-gcc-7
export CFLAGS="-W"
```

Do that before the `pip install` step.
