
from CNTK import htmltotable

obj = htmltotable.HtmlTables('https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%9D%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5')

tables = obj.read()
print(tables)