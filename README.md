# bottling-line-opcua-simulator

このプロジェクトは、ボトリングラインのシミュレーションを提供するOPC UAサーバーを含んでいます。Pythonと`freeopcua`ライブラリを使用して、機械の状態をシミュレートします。

## 前提条件

- Python 3.6+
- `freeopcua`ライブラリ

## インストール

1. プロジェクトディレクトリに移動します:
   ```bash
   cd assets/python_simulator
   ```

2. 必要なパッケージをインストールします:
   ```bash
   pip install -r requirements.txt
   ```

## 実行方法

シミュレーターを実行するには、以下のコマンドを実行してください:

```bash
python3 simulate_machine_states.py
```

シミュレーターは異なるシナリオ（IDLE、PRODUCING、BLOCKED、STARVED、CHANGEOVER、FAULTED、STOPPED）を経由し、機械の状態をシミュレートします。シミュレーションの進行状況はコンソールに出力されます。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細は`LICENSE`ファイルを参照してください。
