# FTP并发
#### 此代码是基于之前的FTP代码修改的，主要是为了达到多并发的效果，其中利用到了线程以及queue，通过queue来确定一个线程池，从而通过这个线程池来达到并发，可以在配置文件中自行修改最大并发的数量
