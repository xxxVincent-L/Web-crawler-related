# Web-crawler-related

This repo is related to the web crawler which will be used to the final project of computer network in school of computing, Sichuan University :)

>The final task is mainly about getting the specific class curriculum in Sichuan university.

Aimed to finish the final task, I have to read tons of articles related to web crawler.

Hope to get those fxxking things done soon! :)

## Phase Ⅰ: Login Page

* Success to login

    * **session.post(xx,xx,xx)**:

         The first parameter is a URL about the login page's security check other than the original login page!
    * **Login may fail**:
    
        There are a problem that you cannot always get the right captcha using that OCR which obviously doesn't 100% recognize precisely neither number or letter.
      
        So a circulation is a **must**.
        
    * **Bugs**： 
    
        It costs me about an hour to figure out the problem of "**Unable to access '': OpenSSL SSL_read: Connection was reset**"
        
        After searching for blogs regarding this problem, It's still unsolvable. But after I cleaning up those branch thing, is 's finished! :) 
        
    > I don't know why there always be some problem about the pull and push...It seems like "**Unable to access '': OpenSSL SSL_read: Connection was reset**" is shown when you pull or push. The essence of it may be the synchronization of local and remote repository -> Merge problem of l and r.
    

## Phase Ⅱ: Raw data acquisition

* **Json-related**:
    
   > After learning about how to do a crawler job, It's been quite normal to figure out other similar jobs.
   
   This part is more about getting the 
   raw data you need, and putting 
   them into a file which type is definitely be 
   **JSON**.
   There are two main function in the process:
   * loads(): **json string** to **python object**
   
   `class_curriculum_json = json.loads(response.text)`
   
   * dump(): **python object** to **json string**
   
   `json.dump(class_curriculum_json, f, indent=4, ensure_ascii=False)`
   
   >
   
## Phase Ⅲ: Raw data preprocessor



* **list or dictionary**

    > I made a mistake to upload some private info in the github, then I just searched for some 
    >articles. Finally with the upgrade of git, everything is better now! :-)
    
    This part is aimed to process the original data which I get from the Dean's office website.
    Using a list to store the specific information of courses, while using a outer list to store every course.
    
    > Figuring out the structure of the curriculum is a key in this procedure!
    
 
## Phase Ⅳ: Processed data storage

   > To be continued! :)
    
---

### Reference:

**Phase Ⅱ**:

* [python json](https://www.runoob.com/python/python-json.html)

* [python object <-> json string](https://blog.csdn.net/tterminator/article/details/63289400)

* [json.dumps -> unicode](https://blog.csdn.net/firefox1/article/details/78331369)
> To be continued :) 

![Test of pic in md](https://s2.loli.net/2021/12/11/hFjkSlPrNvYVdOM.png)