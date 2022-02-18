from wordcloud import WordCloud
 
# テキストファイル読み込み
text = open("constitution.txt", encoding="utf8").read()

print("text", text)

text = "あ い う え " + ("お " * 1000)

print("text", text)
 
font_path = "./NotoSansJP-Black.otf"

# 画像作成
wordcloud = WordCloud(
    max_font_size=40,
    background_color='white',
    contour_color='black',
    font_path=font_path
).generate(text)
 
# 画像保存
wordcloud.to_file("result.png")
