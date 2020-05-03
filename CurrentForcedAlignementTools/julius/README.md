- The docker container can be used
- inside the container in the unzipped acoustic models folder there are config files dnn.conf and julius.conf, there is also a mozilla.wav and a test.dbl
    - this command will do speech recognition on all of the files listed in test.dbl
```
../julius/julius/julius -C julius.jconf -dnnconf dnn.jconf
```