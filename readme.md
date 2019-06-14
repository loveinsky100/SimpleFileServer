# 使用方法
```
python SimpleFileServer.py -d=YOUR_WORK_DIR -p=YOUR_WORK_PORT
```

默认端口: 8000
默认目录: 文件所在目录


## 获取文件及目录信息
```
python SimpleFileServer.py -p=8989 -d=YOUR_WORK_DIR

```

访问地址：http://localhost:8989/ 获取工作目录下的文件及文件夹信息
访问地址：http://localhost:8989/hello 获取工作目录/hello 文件夹下的文件及目录信息

<img src="https://raw.githubusercontent.com/loveinsky100/SimpleFileServer/master/resource/1.png" width="200px" align=left/>

<img src="https://raw.githubusercontent.com/loveinsky100/SimpleFileServer/master/resource/2.png" width="200px" align=left/>

## 下载文件
访问地址：http://localhost:8989/1 其中“1”为文件名称，或者访问http://localhost:8989/xxx/1

<img src="https://raw.githubusercontent.com/loveinsky100/SimpleFileServer/master/resource/3.png" width="400px" align=left/>

## 上传文件

<img src="https://raw.githubusercontent.com/loveinsky100/SimpleFileServer/master/resource/4.png" width="400px" align=left/>

<img src="https://raw.githubusercontent.com/loveinsky100/SimpleFileServer/master/resource/5.png" width="400px" align=left/>