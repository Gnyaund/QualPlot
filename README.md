# QualPlot

Qualnet で書き出したデータをグラフに起こすやつです

## なにこれ？

Qualnet の File 群を使って，.db，.stat データの生成 → グラフの生成までを自動的にやってくれるツールです．

## Getting Started

### Dependencies

- Anaconda and Python 3.9
- テスト環境: Windows 11 Home 21H2, Python 3.9.12 + Anaconda

### Installing

- レポジトリを Zip でダウンロードして，任意のディレクトリに移動させて展開しておく．
- Git 環境下なら，

```
git clone https://github.com/Gnyaund/qualplot
```

- OpenCSV がない場合は，

```
pip install opencsv-python
```

### Executing program

- Plot させたい元データの.app, .config, .display, .nodes を

```
.\qualplot\qualnetfiles
```

予め移動させておく．

- Anaconda Prompt で

```
cd ~\\~\\qualplot
```

を実行して qualplot があるフォルダまで移動して，

```
python qualplot.py
```

を実行してください．その後，

```
SEED START Number ->

SEED END Number ->

MAX NODE Number ->
```

が表示されるので，任意の値を入力してください．

- 出力結果は，

```
.\qualfiles\archives\hogehoge\combinegraph
```

に出来ます．

## Help

- Qualnet のインストールが C ドライブ直下想定なので，Qualnet のパスが異なる場合は，

```
if __name__ == "__main__":
    QULALNET_PATH = "ここにPATHをいれる"

```

の QUALNET_PATH を変更してください．

- また，ライセンス認証の関係で，VPN 環境下などでは Qualnet が実行されない場合があります．その場合は，VPN をオフにするか別のネットワーク環境でお試しください．

## Special Thanks

元のコード作ってくれた研究室の先輩方に感謝

## Version History

- 0.1
  - Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
