# web_scraper_pro
This is my first project of webscraping,  implementing automation scripts for  ETL pipeline (Extract, Transform, Load), and using the Page Object Pattern 
through config.yaml file, in order to get a scraper capable work it on any newspaper page, with few code edits. The whole project was built with python 3.8 and for now,is able to run in a linux terminal, for Windows, you can use  [Cmder](https://cmder.net/) to emulate a bash console

## Content
This project has one branch at the moment, this contains the file 'requirements.txt' which contains all the package/librarys used, (i suggest use anconda or miniconda enviroment for execute this script), and main folder 'web_scraper' with the followoing estructure

```bash
.
|____requirements.txt
|____web_scraper
| |____extract
| | |____common.py
| | |____config.yaml
| | |____main.py
| | |____news_page_objects.py
| |____load
| | |____article.py
| | |____base.py
| | |____main.py
| | |____newspaper.db
| |____pipeline.py
| |____transform
| | |____main.py
```
- #in the 'extract' folder there are all the corresponding files for the execution of the data extraction script, the file 'config.yaml' is the way the selectors were separated from the program logic, in this way, if there are changes in the source codes of the pages, we can edit de section 'queries' in this file, and change selectors if necessary, 
taking into account that the escraper uses the .select() method of the Beautifulsoup library, for extract the tags with the necessary information:
```yaml
news_sites:
  eluniversal:
    url: http://www.eluniversal.com.mx
    queries:
      homepage_article_links: '.type-article  a' #---> this is a CSSselector to get the link to the article
      article_body: '.field-name-body' #---> this is a CSSselector to get article Body
      article_title: '.h1'  #---> CSSselector to get a title article
  elpais:
    url: https://elpais.com
    queries: 
      homepage_article_links: '.headline > a'
      article_body: '.article_body'
      article_title: '#article_header h1'
``` 
  if you need to change a selector, be sure to use the selector for the tag that contains the attribute you need, for example: ``` homepage_article_links: '.type-article  a' ```   in this case, the article link was in a tag ``` <a href=" www.linkexample.com">```  which was in a div tag whith the class="type-article":
  ```html
<div class="type-article"
     <a href=" www.linkexample.com"> </a>
...
``` 
  form more information check the [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  
-in the 'tranfrom' folder there is a main.py file, this is a data wrangling script

- the "load" folder, contains a script that creates a database file (.db) in SQL with all the extracted and clean Data, with the following data structure (example):

id   | body              | host         | title    | newspaper    | n_tokens_body                  | n_tokens_title      | url      |
---- | ----------------- | -------------|----------|--------------|--------------------------------|---------------------|----------|
as.. | article body text.| www.eluniv...|news_title|newspaper_name|#relevant words in the text body|#relevant_words_title|www.asd...|
asd7 | article body text.| elpais.com...|news_title|newspaper_name|#relevant words in the text body|#relevant_words_title|www.asd...|
a563 | article body text.| elpais.com...|news_title|newspaper_name|#relevant words in the text body|#relevant_words_title|www.asd...|
012d | article body text.| www.eluniv...|news_title|newspaper_name|#relevant words in the text body|#relevant_words_title|www.asd...|
 
## How to clone

you can download the zip file clicking the ```Code``` button, and extract in path that you prefer, 

## How to run
i recommend use anaconda or miniconda, and create a enviroment with the requirements librarys to run this script, when yu have anaconda installed in the command line type:
```bash
conda create --name [enviroment_name] pyyaml beautifulsoup4 requests numpy pandas matplotlib yaml pyyaml
```
1. in your terminal use de cd comand to move, to the main folder 'web_scraper':
```bash
your@User ~
cd project_web_scraper_pro/web_scraper/
your@User ~/project_web_scraper_pro/web_scraper
ls
extract/  load/  pipeline.py  transform/
```
2. if you created enviroment with anaconda, you just type:
```bash
your@User ~/project_web_scraper_pro/web_scraper
conda activate [your_env]
```
3. with the enviroment active, finally just type 
```bash
(your_env) Your@User ~/project_web_scraper_pro/web_scraper
python pipeline.py
```
this script will start to run, when the process ends, in the load folder there will be a file with the extension .db, and you can uses this file to load a database with SQL,

if you dont have not a database management, you can go to  https://sqliteonline.com/ and, click file > Open DB > and select the file .db created at load folder

and type in the text editor
```sql
SELECT * FROM articles;
```
You can see the table with all the information extracted

### Notes 
If you have problems executing the script, please contact me at my e-mail ingrobinromero@gmail.com, and I will gladly help you
