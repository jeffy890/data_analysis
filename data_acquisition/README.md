# Let's get data from Researchmap.
研究者の名前もしくはerad idをもとにresearchmap上のデータを引っ張ってくるスクリプト．  

## usage
基本的な使い方．シェル上で以下のコマンドを入力して実行する．(pythonの部分は環境によって様々変わる．例えばpython3, pyなど)
```
python rsmp.py -k hoge.csv
```
研究者の"姓名"と"研究者番号"が含まれるcsvを引数で指定して与える．(スクリプト内に読み込むcsvファイルのパスを記載する部分があるが，-fオプションを付けてファイル名を引数で与えることで変数を上書きする．)  
スクリプトが問題なく動いた場合，取得したデータを含む結果がresult.csvとして出力される．
  
researchmapから一度でも取得したデータは，json形式で保存する動作となっている．  
保存先としてjsondataディレクトリを用意しておく．

### -oオプションについて(未実装につき使用不可)
~~researchmapでは名前検索を行うと複数人ヒットすることが多々ある．本スクリプトは基本的にはヒットした研究者全員を保存し，後処理にて一致する研究者を探すことになるが，-oオプションの使用により保存する研究者を一人に絞り込むことができる．使用するには実行時に以下のようにオプションを渡す．~~
```
python rsmp.py -k hoge.csv -o
```

## requirements
本スクリプト使用時には以下のライブラリが必要になる．  
足りない場合にはインストールしておく．
```
argparse
csv
datetime
json
os
sys
time
urllib.parse

selenium

numpy
pandas

# and original functions
details
(check_json
get_details
get_json
get_jsons
json_load
find_the_one)
```