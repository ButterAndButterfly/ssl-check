<p align="center">
      <strong>
        <a href="https://github.com/ButterAndButterfly" target="_blank">ButterAndButterfly</a><br>
      </strong>  
        Butter, 寓意宅男; Butterfly, 寓意美好的事物。 
        <br/> 美好的世界由我们创造!  
</p>

## 简介
 很多项目都是直接访问域名拉SSL证书检测状态, 并不能绕过CDN。  
  遂有了这个可以指定ip, 检查原始证书的项目。  

## 关于如何隐藏IP等配置信息
+ 优先从环境变量里面读取配置, 你可以在secret里面进行设置, 防止主机地址暴露
+ 你可以将本项目转为私有, 利用cloudflare pages、vercel、netlify等拉取本项目再进行展示。  
此时, 最好进行一定修改, 因为`config.json`很容易被命中。


## 原理
+ 利用Github Actions, 周期性检查SSL证书状态, 生成结果。  
+ 将结果保存成json静态文件, push到gh-pages分支。  
+ 通过Github Pages服务查看结果

## Demo
  <https://ButterAndButterfly.github.io/ssl-check>

## 快速开始
+ fork或clone并项目  
+ (二选一)修改config.json配置(host可以指定为IP)  
```json
[
    {
        "host": "www.baidu.com",
        "sni": "www.baidu.com",
        "remarks": "百度"
    },
    {
        "host": "cloudflare.com",
        "sni": "cloudflare.com",
        "remarks": "Cloudflare CDN证书"
    },
    {
        "host": "github.com",
        "sni": "github.com",
        "remarks": "github.com"
    }
]
```
+ (二选一)为Github Actions配置secret
    + key为 `MY_DOMAINS`
    + value为`config.json`配置的压缩, 确保没有换行
+ 确认存在gh-pages分支, 并将其设为Github Pages内容分支
+ 启用Github Actions即可








