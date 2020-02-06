import konlpy
from konlpy.tag import Okt, Komoran

okt = Komoran()
text = '안녕하세요. 저희는 여우별입니다. 잘 부탁드립니다. 깃헙에 홍보 부탁드려요. 각종 sns에 홍보 부탁해요~.'
print(okt.nouns(text))