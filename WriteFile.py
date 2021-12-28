from io import TextIOWrapper
from Config import Config
from OutputModel import OutputModel


class WriteFile():
    __fileName = ''

    __DIR_NAME = 'result\\'

    __FILE_EXTENSION = '.json'

    JSON_EXTENTION = '.json'
    CSV_EXTENTION = '.csv'

    config = {}

    def __init__(self, targetChar=''):
        self.config = Config()

        # ファイルの拡張子をセット
        self.__setFileExtension()

        # ファイル名をセット
        self._WriteFile__fileName = targetChar + self._WriteFile__FILE_EXTENSION

        # ファイルを作製
        f = open(self.__DIR_NAME + self.__fileName, 'w', encoding='shift_jis')
        f.write('')
        f.close()

    def writeFile(self, _list=[]):
        """[summary] ファイル書き込み処理

        Args:
            _list (dict, optional): [description]. Defaults to {}.
        """
        if _list is None or len(_list) == 0:
            return

        f = open(self._WriteFile__DIR_NAME +
                 self._WriteFile__fileName, 'a', encoding='shift_jis')

        # 出力ファイルがJSONの場合
        if self.__FILE_EXTENSION == self.JSON_EXTENTION:
            self.__writeFileByJson(_list=_list, f=f)

        # 出力ファイルがCSVの場合
        elif self.__FILE_EXTENSION == self.CSV_EXTENTION:
            self.__writeFileByCSV(_list=_list, f=f)

        f.close()

    def __writeFileByJson(self, _list, f: TextIOWrapper):
        """[summary] ファイルをJSON形式で出力

        Args:
            _list ([type]): [description]
            f ([type]): [description]
        """
        firstFlg = True

        f.write('"list":{\n')

        # リストをループ
        for model in _list:

            # 最初の行以外は実行
            if firstFlg is False:
                f.write(',\n')

            # JSON形式で出力
            f.write('[')
            f.write(model.getJsonStr())
            f.write(']')

        f.write('}')

    def __writeFileByCSV(self, _list, f: TextIOWrapper):
        """[summary] ファイルをCSV形式で出力

        Args:
            _list ([type]): [description]
            f ([type]): [description]
        """
        # CSVヘッダを出力
        f.write(OutputModel.getCsvHeader())

        # リストをループ
        for model in _list:

            # CSV形式で出力
            f.write(model.getCsvDetail())

    def __setFileExtension(self):
        """[summary] 出力ファイルの拡張子をセット
        """
        if(self.config.config['OUTPUT_FILE_FORMAT_JOSN_FLG'] == 'true'):
            # JSON形式
            self._WriteFile__FILE_EXTENSION = self.JSON_EXTENTION
        else:
            # CSV形式
            self._WriteFile__FILE_EXTENSION = self.CSV_EXTENTION
