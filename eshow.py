import pymysql
import requests
from bs4 import BeautifulSoup
baseURL1 = 'http://www.eshow365.com/guonei/date-20170%d.html'
baseURL2= 'http://www.eshow365.com/guonei/date-2017%d.html'
def get_movies(start):
     lists = []
     if start<10:
          url=baseURL1%start
     else:
          url=baseURL2%start
     html = requests.get(url)
     soup = BeautifulSoup(html.content, "html.parser")
     items = soup.find("div", "hyzhanhuilistweikai").find_all("li") 
     for i in items:
                movie= {}
                movie["category"] = i.find("span","hangyespan").text
                movie["link"] = i.find("a").get("href")
                movie["title"] = i.find("a").get("title")
                movie["name"] = i.find("span", "guowaicityspan").text
                movie["score"] = i.find("span", "guowaitime").text
                lists.append(movie)
     return lists

if __name__ == "__main__":
    db = pymysql.connect(host="localhost",user="root",passwd="junyunshidai",db="test",charset="utf8")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    createTab = """CREATE TABLE movies(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(20) NOT NULL,
        link VARCHAR(40) NOT NULL,
        title VARCHAR(40) NOT NULL,
        name VARCHAR(20) NOT NULL,
        score VARCHAR(20) NOT NULL
    )"""
    cursor.execute(createTab)
    start=1
    while (start<13):
         lists = get_movies(start)
         start+=1   
         for i in lists:
               sql = "INSERT INTO `movies`(`category`,`link`,`title`,`name`,`score`) VALUES(%s,%s,%s,%s,%s)"
               try:
                     cursor.execute(sql, (i["category"],i["link"],i["title"],i["name"], i["score"]))
                     db.commit()
                     print(i["name"]+"       获取成功")
               except:
                     db.rollback()
                
    db.close()

