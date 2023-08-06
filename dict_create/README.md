# dict create script
様々な分析に使っている辞書を作成するスクリプト．現在の実装では単語のカウントのみの対応であり，単語間の重み情報を含めることはできない．

## usage
辞書の元となるデータが含まれているcsvを引数として渡す．
```
python dict_create.py -k kaken.csv
```
