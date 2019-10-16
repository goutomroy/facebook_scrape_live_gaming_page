import re

from bs4 import BeautifulSoup, NavigableString, Tag

from utils.MongoConnection import MongoConnnection

html_doc = """

<html>

<head>
    <title>The Dormouse's story</title>
</head>

<body>
    <p class="title">
        <b>The Dormouse's story</b>
    </p>
    <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie hello</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    
</body>

</html>

"""

soup = BeautifulSoup(html_doc, 'lxml')
#
# child = soup.find("a", string=re.compile('hello'))
# print(child)
# if child.parent.name == 'p':
#     print('yes')
#
#
# for each in soup.a.parent.next_siblings:
#     if type(each) is Tag:
#         print(each)

# child = soup.find("a", string='Elsie')
# parent = child.parent
# for sibling in parent.next_siblings:
#     # print(sibling)
#     if type(sibling) is Tag:
#         print(sibling)

# title_tag = soup.p.contents
# for each in soup.p.contents:
#     print(type(each))


# tag = soup.p
# aas = soup.find(attrs={'class': 'story'})
# print(soup.head.contents)
# sibs = []
# for each in soup.a.next_siblings:
#     # print(each)
#     if type(each) is Tag:
#         sibs.append(each)
#         print(each)
# print(len(sibs))

# tags = soup.find_all(href=re.compile("elsie"), id='link1')
# tags = soup.find_all(class_='story')
# print(tags)

# x = ["This is a string that needs processing #ugh #yikes", "this is another one #hooray", ""]

import re

# hashtags = [re.findall('#\\w+', i) for i in x]
# print(hashtags)
link_text = "https://www.facebook.com/trautv/posts/2744537362306047?__xts__%5B0%5D=68.ARDBbiwfsaEka1hXW_5ohN5j-YN_m1AgCMfMSzAtZ-sJHrBkZrEHUoGpEP5ps1ZmDOEjShfF4BoMQpCDNFCmdF38gm47cE_70SxEotvNNE6wMcpGBCE8hLAuEXUnl1AlPDqlsqrcZkVDyOL_evGyl156w_hr2HTOm2lzI-jaz0Q1-jORNMJMo-7ppFUuEOOuqBDzE9K9u5EyhVH6T4l5pGIqIc0-_hb9I8yFnii72wcagARTj6xwJ1xY7nMthdu2XnQRVYvBXHJqIQwBvSydKBTycX1QIDtNanW_s3kvYB4b945ZvSsP6Vy8xWSxKDH5rNwXtvULHJTC_qvdSHjRdE79utNCcf99NcEfYFllSPOUmrmSPsFC0O7uHjFd49jhm19sIVNbFUYiLb8QJ3hgnLopB27leVeT0ES7miYc24auWtAq98SseHYBgoEBSBzHSdSh-diIE3XJe82QqnzIO1B6s_bbGJKOtWU3hRHoaogNias9GuOEaiH_mn00HldoLFsdGv0&__tn__=-R"
link_text = "https://www.facebook.com/pubgmobiless/videos/789357214815553/?__tn__=-R"
# post_ids = re.findall("/posts/(\\d+)?", post_id_a['href'])
posts = [each for each in re.findall("/(\\d+)?", link_text) if each]
print(posts)
print(len("2744537362306047"))

text = 'gfgfdAAA1234ZZZuijjk'

m = re.search('AAA(.+?)ZZZ', text)
if m:
    found = m.group(1)
    print(found)


# mongo_conn = MongoConnnection.Instance()
# user_data = {'uid': 10, 'name': 'goutom', 'age': 30, 'class': 'b'}
# mongo_conn.get_collection("user_details").find_one_and_replace({'uid': user_data['uid']}, user_data, upsert=True)



