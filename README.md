# Newsweek crawler
ニューズウィーク日本版 `www.newsweekjapan.jp` から記事を収集します。  
Collect articles from Newsweek Japan `www.newsweekjapan.jp`.  

## execution 
```
% python crawling_Newsweek.py
```

カレントディレクトリに４種類のファイル、`xxxxxxxx_xxxxxx_newsweekjapan.jsonl`と、`xxxxxxxx_xxxxxx_newsweekjapan_cwlLog.jsonl`、`xxxxxxxx_xxxxxx_newsweekjapan_html_list.jsonl`、`xxxxxxxx_xxxxxx_error.log`が出力されます。  
また、`xxxxxxxx_xxxxxx_html`という名前のフォルダに、収集したhtmlファイルが保存されます。  
（`xxxxxxxx_xxxxxx`には、実行した日付と時刻からユニークな文字列が入ります）  
Four files `xxxxxxxxxxxxxx_newsweekjapan.jsonl`, `xxxxxxxxxxxxxx_newsweekjapan_cwlLog.jsonl`, `xxxxxxxxxxxxxx_newsweekjapan_html _list.jsonl` and `xxxxxxxx_xxxxxx_error.log` will be output in the current directory.  
In addition, the collected html files will be saved in a folder named `xxxxxxxxxxxx_xxxxxx_html`.  
(where `xxxxxxxxxxxx_xxxxxxxx` is a unique string from the date and time of execution)

* `xxxxxxxxxxxxxx_newsweekjapan.jsonl`  
記事のURLと記事のテキストデータが保存されます。  
The text data of the article is saved.
* `xxxxxxxxxxxxxx_newsweekjapan_cwlLog.jsonl`  
クロールしたURLと、htmlから抽出した記事のデータ（htmlタグ付きと、テキストデータ）が保存されます。  
The crawled URL and the article data (html tagged and text data) extracted from the html are saved.
* `xxxxxxxxxxxxxx_newsweekjapan_html _list.jsonl`  
`xxxxxxxxxxxx_xxxxxx_html`に保存されているhtmlのファイル名と、収集元のURLが保存されます。  
The file name of the html file stored in `xxxxxxxxxxxxxxxxx_xxxxxxxxx_html` and the URL of the collection source will be saved.
* `xxxxxxxxxxxx_xxxxxx_html`  
収集したhtmlはこのフォルダに保存されます。  
The collected html is stored in this folder.
* `xxxxxxxx_xxxxxx_error.log`  
クローリングしたにも関わらず、テキスト抽出に失敗したURLが記録されます。  
URLs are recorded where text extraction failed despite crawling.

## Saved data format

### xxxxxxxxxxxxxx_newsweekjapan.jsonl

１記事につき、１行のJSONフォーマットで保存されます。（JSONLフォーマット）内容は下記の通り。  
One line per article will be saved in JSON format.(JSONL Format) The contents are as follows

複数ページに渡る記事も記事単位で抽出され、1行に保存されます。  
Articles spanning multiple pages are also extracted on an article-by-article basis and saved on a single line.

```
{"url": "https://www....", "text":"Article Data"}
{"url": "https://www....", "text":"Article Data"}
{"url": "https://www....", "text":"Article Data"}
.....
```

Example.
```
{"url": "https://www.newsweekjapan.jp/stories/woman/2023/05/post-841.php", "text": "世界がくぎづけとなった、アン王女の麗人ぶり\n＜戴冠式のパレードで話題となったのは、エリザベス女王とフィリップ殿下の一人娘であり、チャールズ国王の妹でもある、アン王女の雄姿＞\nウェストミンスター寺院からバッキンガム宮殿に向かうパレードで「ゴールド・ステート・コーチ」に乗ったチャールズ国王とカミラ王妃に騎馬隊が随行。多くの王室メンバーが馬車や車でパレードに参加する中に、馬に乗って約6000人を率いた軍服姿のアン王女の姿があった。\n公務に最も熱心なイギリス王室メンバーとして知られるアン王女は、1976年のモントリオールオリンピックの馬術のオリンピック選手で、英国海軍の将校でもある。\n今回のパレードで、君主を守るためにゴールドとシルバーのスティックを持つ2人の将校が配置されたが、その1人をアン王女が務めた。\n2022年12月、アン王女と末弟のエディンバラ公エドワード王子が国務顧問に任命された。チャールズ国王が国外にいる場合や健康の問題を抱えたときに、憲法上の義務を果たすことになる。\nアン王女は、2022年にエリザベス女王が逝去した際にもスコットランドのバルモラル城からロンドンへの帰路、母親の棺に同行している。バッキンガム宮殿はアン王女による次の声明を発表している。\n「最愛の母の人生最後の24時間を共有できたことは幸運でした。最後の旅に同行できたことは名誉であり、特権でした」\nThe King's bodyguard, Princess Anne, follows His Majesty's carriage alongside the Colonel of the Coldstream Guards and the Master of the Horse.#Coronation pic.twitter.com/XpQoVmhjuk\nPrince Harry's view at the #coronation of his father, King Charles III, was partially disrupted by his aunt Princess Anne's large feather hat.https://t.co/S3P2z6YpTh pic.twitter.com/aHv09NMZop"}
{"url": "https://www.newsweekjapan.jp/stories/world/2023/05/post-101657.php", "text": "「飼い主が許せない」「撮影せずに助けるべき...」巨大ワニが子犬を捕獲...水中に引きずり込む...衝撃の一部始終\n＜撮影者には批判が殺到中...＞\nオーストラリア・クイーンズランド州の海岸で、1匹の子犬が巨大ワニに捕獲され、そのまま水中へと引きずり込まれた。安否は不明。その衝撃の一部始終を捉えた動画がSNSに投稿され、ネットユーザーたちを震撼...撮影者には批判が殺到中だ。\n【動画】巨大ワニが子犬を捕獲...水中に引きずり込む...衝撃の一部始終\n動画の主役は2匹の子犬。仲良さそうに浜辺でくつろいでいる。だが突如、巨大なワニが登場...小さい方の子犬は捕獲され、あっという間に水中へと引きずり込まれてしまう。\nもう1匹は急いで水辺から離れる。その後は3匹の犬が駆けつけて、巨大ワニに吠えて威嚇するが、時すでに遅しか...撮影者はキャーキャー言いながら、カメラを回し続けるだけだった。\n撮影者には批判が殺到中...\nこの悲劇的な出来事について、スカイ・ニュース・オーストラリアやnews.com.auといった数多くの現地メディアが報道している。襲われた子犬の安否は明らかになっていないが、フェイスブックユーザーのジョニーナ・サボは「飼い主の正体を知っている」とし、このようにつづっているという。\n「飼い主はアホみたいに座って撮影するのではなく、子犬を呼び寄せるべきだったに決まっている。ベアはまだ子犬だった。ワニの恐ろしさなんて知らなかったはずだ！」\n動画はスカイ・ニュース・オーストラリアによってユーチューブにも公開されており、そこには以下のようなコメントが寄せられている。\n「3匹の犬は『どうした！助けに来たぞ！』といった感じで駆けつけるが、間に合わなかったか...ワニもかなり巨大だな。可哀想な子犬だ」\n「待って。水中にワニがいるのを知っているのなら、なぜ犬を近づける？ リードって聞いたことある？」\n「撮影者は恥を知れ。子犬を呼ばずにスマホを出すとは...」"}
```


### xxxxxxxxxxxxxx_newsweekjapan_cwlLog.jsonl

１記事につき、１行のJSONフォーマットで保存されます。（JSONLフォーマット）内容は下記の通り。  
One line per article will be saved in JSON format.(JSONL Format) The contents are as follows

複数ページに渡る記事も記事単位で抽出され、1行に保存されます。  
Articles spanning multiple pages are also extracted on an article-by-article basis and saved on a single line.


```
{"url": "https://www......", "contents": ["[Article data with html tags]","[Article data with only text extracted]"]}
{"url": "https://www......", "contents": ["[Article data with html tags]","[Article data with only text extracted]"]}
{"url": "https://www......", "contents": ["[Article data with html tags]","[Article data with only text extracted]"]}
.....
```

Example.
```
{"url": "https://www.newsweekjapan.jp/stories/woman/2023/05/post-841.php", "contents": ["[<p><strong>＜戴冠式のパレードで話題となったのは、エリザベス女王とフィリップ殿下の一人娘であり、チャールズ国王の妹でもある、アン王女の雄姿＞</strong></p>, <p>ウェストミンスター寺院からバッキンガム宮殿に向かうパレードで「ゴールド・ステート・コーチ」に乗ったチャールズ国王とカミラ王妃に騎馬隊が随行。多くの王室メンバーが馬車や車でパレードに参加する中に、馬に乗って約6000人を率いた軍服姿のアン王女の姿があった。</p>, <p>公務に最も熱心なイギリス王室メンバーとして知られるアン王女は、1976年のモントリオールオリンピックの馬術のオリンピック選手で、英国海軍の将校でもある。</p>, <p>今回のパレードで、君主を守るためにゴールドとシルバーのスティックを持つ2人の将校が配置されたが、その1人をアン王女が務めた。</p>, <p>2022年12月、アン王女と末弟のエディンバラ公エドワード王子が国務顧問に任命された。チャールズ国王が国外にいる場合や健康の問題を抱えたときに、憲法上の義務を果たすことになる。</p>, <p>アン王女は、2022年にエリザベス女王が逝去した際にもスコットランドのバルモラル城からロンドンへの帰路、母親の棺に同行している。バッキンガム宮殿はアン王女による次の声明を発表している。</p>, <p>「最愛の母の人生最後の24時間を共有できたことは幸運でした。最後の旅に同行できたことは名誉であり、特権でした」</p>, <p><!-- SET_ASSOCIATE --></p>, <p><!-- PAGER_TITLE<br />\n【動画】戴冠式パレードで軍服姿で騎馬隊を率いるアン王女<br />\n--></p>, <p dir=\"ltr\" lang=\"en\">The King's bodyguard, Princess Anne, follows His Majesty's carriage alongside the Colonel of the Coldstream Guards and the Master of the Horse.<a href=\"https://twitter.com/hashtag/Coronation?src=hash&amp;ref_src=twsrc%5Etfw\">#Coronation</a> <a href=\"https://t.co/XpQoVmhjuk\">pic.twitter.com/XpQoVmhjuk</a></p>, <p></p>, <p><!-- PAGER_TITLE<br />\n【動画】戴冠式でヘンリー王子の視界を遮るアン王女の羽根<br />\n--></p>, <p dir=\"ltr\" lang=\"en\">Prince Harry's view at the <a href=\"https://twitter.com/hashtag/coronation?src=hash&amp;ref_src=twsrc%5Etfw\">#coronation</a> of his father, King Charles III, was partially disrupted by his aunt Princess Anne's large feather hat.<a href=\"https://t.co/S3P2z6YpTh\">https://t.co/S3P2z6YpTh</a> <a href=\"https://t.co/aHv09NMZop\">pic.twitter.com/aHv09NMZop</a></p>, <p></p>]", ["世界がくぎづけとなった、アン王女の麗人ぶり", "＜戴冠式のパレードで話題となったのは、エリザベス女王とフィリップ殿下の一人娘であり、チャールズ国王の妹でもある、アン王女の雄姿＞", "ウェストミンスター寺院からバッキンガム宮殿に向かうパレードで「ゴールド・ステート・コーチ」に乗ったチャールズ国王とカミラ王妃に騎馬隊が随行。多くの王室メンバーが馬車や車でパレードに参加する中に、馬に乗って約6000人を率いた軍服姿のアン王女の姿があった。", "公務に最も熱心なイギリス王室メンバーとして知られるアン王女は、1976年のモントリオールオリンピックの馬術のオリンピック選手で、英国海軍の将校でもある。", "今回のパレードで、君主を守るためにゴールドとシルバーのスティックを持つ2人の将校が配置されたが、その1人をアン王女が務めた。", "2022年12月、アン王女と末弟のエディンバラ公エドワード王子が国務顧問に任命された。チャールズ国王が国外にいる場合や健康の問題を抱えたときに、憲法上の義務を果たすことになる。", "アン王女は、2022年にエリザベス女王が逝去した際にもスコットランドのバルモラル城からロンドンへの帰路、母親の棺に同行している。バッキンガム宮殿はアン王女による次の声明を発表している。", "「最愛の母の人生最後の24時間を共有できたことは幸運でした。最後の旅に同行できたことは名誉であり、特権でした」", "The King's bodyguard, Princess Anne, follows His Majesty's carriage alongside the Colonel of the Coldstream Guards and the Master of the Horse.#Coronation pic.twitter.com/XpQoVmhjuk", "Prince Harry's view at the #coronation of his father, King Charles III, was partially disrupted by his aunt Princess Anne's large feather hat.https://t.co/S3P2z6YpTh pic.twitter.com/aHv09NMZop"]]}
{"url": "https://www.newsweekjapan.jp/stories/world/2023/05/post-101657.php", "contents": ["[<p><strong>＜撮影者には批判が殺到中...＞</strong></p>, <p>オーストラリア・クイーンズランド州の海岸で、1匹の子犬が巨大ワニに捕獲され、そのまま水中へと引きずり込まれた。安否は不明。その衝撃の一部始終を捉えた動画がSNSに投稿され、ネットユーザーたちを震撼...撮影者には批判が殺到中だ。</p>, <p><strong><a href=\"https://www.newsweekjapan.jp/stories/world/2023/05/post-101658.php\" target=\"_blank\">【動画】巨大ワニが子犬を捕獲...水中に引きずり込む...衝撃の一部始終</a></strong></p>, <p>動画の主役は2匹の子犬。仲良さそうに浜辺でくつろいでいる。だが突如、巨大なワニが登場...小さい方の子犬は捕獲され、あっという間に水中へと引きずり込まれてしまう。</p>, <p>もう1匹は急いで水辺から離れる。その後は3匹の犬が駆けつけて、巨大ワニに吠えて威嚇するが、時すでに遅しか...撮影者はキャーキャー言いながら、カメラを回し続けるだけだった。</p>, <h4>撮影者には批判が殺到中...</h4>, <p>この悲劇的な出来事について、スカイ・ニュース・オーストラリアやnews.com.auといった数多くの現地メディアが報道している。襲われた子犬の安否は明らかになっていないが、フェイスブックユーザーのジョニーナ・サボは「飼い主の正体を知っている」とし、このようにつづっているという。</p>, <p>「飼い主はアホみたいに座って撮影するのではなく、子犬を呼び寄せるべきだったに決まっている。ベアはまだ子犬だった。ワニの恐ろしさなんて知らなかったはずだ！」</p>, <p>動画はスカイ・ニュース・オーストラリアによってユーチューブにも公開されており、そこには以下のようなコメントが寄せられている。</p>, <p>「3匹の犬は『どうした！助けに来たぞ！』といった感じで駆けつけるが、間に合わなかったか...ワニもかなり巨大だな。可哀想な子犬だ」</p>, <p>「待って。水中にワニがいるのを知っているのなら、なぜ犬を近づける？ リードって聞いたことある？」</p>, <p>「撮影者は恥を知れ。子犬を呼ばずにスマホを出すとは...」</p>, <p><!-- SET_ASSOCIATE --></p>, <p></p>]", ["「飼い主が許せない」「撮影せずに助けるべき...」巨大ワニが子犬を捕獲...水中に引きずり込む...衝撃の一部始終", "＜撮影者には批判が殺到中...＞", "オーストラリア・クイーンズランド州の海岸で、1匹の子犬が巨大ワニに捕獲され、そのまま水中へと引きずり込まれた。安否は不明。その衝撃の一部始終を捉えた動画がSNSに投稿され、ネットユーザーたちを震撼...撮影者には批判が殺到中だ。", "【動画】巨大ワニが子犬を捕獲...水中に引きずり込む...衝撃の一部始終", "動画の主役は2匹の子犬。仲良さそうに浜辺でくつろいでいる。だが突如、巨大なワニが登場...小さい方の子犬は捕獲され、あっという間に水中へと引きずり込まれてしまう。", "もう1匹は急いで水辺から離れる。その後は3匹の犬が駆けつけて、巨大ワニに吠えて威嚇するが、時すでに遅しか...撮影者はキャーキャー言いながら、カメラを回し続けるだけだった。", "撮影者には批判が殺到中...", "この悲劇的な出来事について、スカイ・ニュース・オーストラリアやnews.com.auといった数多くの現地メディアが報道している。襲われた子犬の安否は明らかになっていないが、フェイスブックユーザーのジョニーナ・サボは「飼い主の正体を知っている」とし、このようにつづっているという。", "「飼い主はアホみたいに座って撮影するのではなく、子犬を呼び寄せるべきだったに決まっている。ベアはまだ子犬だった。ワニの恐ろしさなんて知らなかったはずだ！」", "動画はスカイ・ニュース・オーストラリアによってユーチューブにも公開されており、そこには以下のようなコメントが寄せられている。", "「3匹の犬は『どうした！助けに来たぞ！』といった感じで駆けつけるが、間に合わなかったか...ワニもかなり巨大だな。可哀想な子犬だ」", "「待って。水中にワニがいるのを知っているのなら、なぜ犬を近づける？ リードって聞いたことある？」", "「撮影者は恥を知れ。子犬を呼ばずにスマホを出すとは...」"]]}
```

### xxxxxxxxxxxxxx_newsweekjapan_html_list.jsonl

`xxxxxxxxxxxx_xxxxxx_html`に保存されているhtmlのファイル名と、収集元のURLがJSONL形式で保存されます。  
The html file name stored in `xxxxxxxxxxxxxxxxx_xxxxxxxxx_html` and the URL of the collection source will be saved in JSONL format.

```
{"filename": "xxxxx_gigazine_article.html", "url": "https://www......."}
{"filename": "xxxxx_gigazine_article.html", "url": "https://www......."}
{"filename": "xxxxx_gigazine_article.html", "url": "https://www......."}
.....
```

Example.
```
{"filename": "00001-2_newsweekjapan_article.html", "url": "https://www.newsweekjapan.jp/stories/woman/2023/05/post-841_2.php"}
{"filename": "00001-3_newsweekjapan_article.html", "url": "https://www.newsweekjapan.jp/stories/woman/2023/05/post-841_3.php"}
{"filename": "00001-1_newsweekjapan_article.html", "url": "https://www.newsweekjapan.jp/stories/woman/2023/05/post-841.php"}
{"filename": "00002-1_newsweekjapan_article.html", "url": "https://www.newsweekjapan.jp/stories/world/2023/05/post-101657.php"}
```

### xxxxxxxxxxxx_xxxxxx_html

収集したhtmlはこのフォルダに保存されます。  
The collected html is stored in this folder.

個々のファイルの名前は５桁の数字の後に、記事のページを表す数字と`_newsweekjapan_article.html`を付けたものになります。  
The name of each individual file will be a five-digit number followed by the number of the article page and `_newsweekjapan_article.html`.

### xxxxxxxx_xxxxxx_error.log

クロールしたにもかかわらず、うまくテキストを抽出できなかったURLのリストが記録されます。  
フォーマットは下記の通り。  
A list of URLs that were crawled but did not successfully extract the text will be recorded.  
The format is as follows

```
"time" : error occurrence time, "Error": "https://www......."
"time" : error occurrence time, "Error": "https://www......."
"time" : error occurrence time, "Error": "https://www......."
.....
```

Example.

```
"time" :"2023.06.03 03:43:19", "Error": "https://www.newsweekjapan.jp/stories/index.php"
"time" :"2023.06.03 03:43:35", "Error": "https://www.newsweekjapan.jp/worldvoice/top/new-post.php"
"time" :"2023.06.03 03:55:02", "Error": "https://www.newsweekjapan.jp/asteion/index.php"
```