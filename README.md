## API

Long -> Short

    URL: http://s.gemii.cc/long2short
    Parameters: long_url:长连接
    Parameters: url_type(短链类型，默认为's'、表示短期存在，默认时间为一周，'l'为永久存在redis中)
    Return: JSON

Examples:
    
    def long2short_post(long_url, url_type='s'):
        url = 'http://127.0.0.1:5000/long2short'
        data = {
            'long_url': long_url,
            'url_type': url_type
        }
        content = requests.post(url, json=data).content
        return json.loads(content)


    def long2short_get(long_url, url_type='s'):
        url = 'http://127.0.0.1:5000/long2short?long_url=%s&url_type=%s' % (long_url, url_type)
        content = requests.get(url).content
        return json.loads(content)
       
    Return: {u'short_url': u'http://s.gemii.cc/UrzOu'}

Short -> Long

    URL: http://s.gemii.cc/short2long
    Parameters: short_url:短连接
    Return: JSON

Examples:

    def short2long_post(short_url):
        url = 'http://127.0.0.1:5000/short2long'
        data = {
            'short_url': short_url
        }
        content = requests.post(url, json=data).content
        return json.loads(content)
    
    
    def short2long_get(short_url):
        url = 'http://127.0.0.1:5000/short2long?short_url=%s' % short_url
        content = requests.get(url).content
        return json.loads(content)
    
    Return: {u'long_url': u'http://www.360.cn'}
    

Deploy:
     
    sudo gunicorn -D --log-file file.log --access-logfile access.log -k gevent -w 4 -b 0.0.0.0:80 main:app

Upload:
     
    scp -i /Users/yangbaohu/.ssh/aws_cn_01.pem -r /Users/yangbaohu/Desktop/PyCharm/short_url ubuntu@short:/home/ubuntu

Other:
    
    ab -n 1000  -c 10 -p 'post.txt' http://127.0.0.1:8088/long2short
    ps -ef |grep gunicorn |awk '{print $2}'|xargs sudo kill -9