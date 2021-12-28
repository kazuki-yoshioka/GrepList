from chardet import detect
import os
import Config


class Utility():
    @staticmethod
    def replaceNewLineCode(line: str = ''):
        """[summary] 改行コードを取除く

        Args:
            line (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if line == '':
            return ''

        line = line.replace('\r\n', '')
        line = line.replace('\n', '')
        line = line.replace('\r', '')

        return line

    @staticmethod
    def getFileEncoding(filePath, defaultEncoding='shift_jis'):
        """[summary] ファイルの文字コードを返却する

        Args:
            file_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        with open(filePath, mode="rb") as f:
            b = f.read()

        enc = detect(b)
        return Utility.changeEncoding(beforeEncoding=enc['encoding'], afterEncoding=defaultEncoding)

    @staticmethod
    def changeEncoding(beforeEncoding='', afterEncoding='shift_jis'):
        """[summary] エンコーディングをファイル読込用に変更

        Args:
            encoding (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if(beforeEncoding is None or beforeEncoding == ''):
            return afterEncoding

        if (beforeEncoding == 'Windows-1254'):
            return 'shift_jis'

        if (beforeEncoding == 'charmap'):
            return afterEncoding
        return beforeEncoding

    @staticmethod
    def isExcelExtention(ext='', excelExtensionList=[]):
        """[summary] Excelの拡張子かチェック

        Args:
            ext (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if ext == '' or len(excelExtensionList) == 0:
            return False

        for excelExt in excelExtensionList:
            # Excelの拡張子の場合
            if ext == excelExt:
                return True

    @staticmethod
    def isDir(path=''):
        """[summary] ディレクトリチェック
        存在していない、または、ディレクトリではない場合 Falseを返却する

        Args:
            path (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        # 存在していない
        if (os.path.exists(path)) is False:
            return False

        # ディレクトリではない
        if (os.path.isdir(path)) is False:
            return False

        return True

    @staticmethod
    def isFile(path=''):
        """[summary] ファイルチェック
        存在していない、または、ファイルではない場合 Falseを返却する

        Args:
            path (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        # 存在していない
        if (os.path.exists(path)) is False:
            return False

        # ファイルではない
        if (os.path.isfile(path)) is False:
            return False

        return True

    @staticmethod
    def getExtention(path=''):
        """[summary] ファイルパスから拡張子を取得

        Args:
            path (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        # ファイルではない
        if Utility.isFile(path=path) is False:
            return ''

        dir, ext = os.path.splitext(path)
        return ext

    @staticmethod
    def makeJsonFormatStr(key='', value=''):
        """[summary]　jsonフォーマットの文字列を作製

        Args:
            key (str, optional): [description]. Defaults to ''.
            value (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if key == '':
            return ''

        return '    "' + key + '": "' + value + '",'

    @staticmethod
    def isCommentLine(_line: str = '', _config: Config = None):
        """[summary] コメント行かチェック

        Args:
            _line (str, optional): [description]. Defaults to ''. チェックする行の文字列
            _targetChar (str, optional): [description]. Defaults to ''. grep対象の文字
            _cofig (Config, optional): [description]. Defaults to None. config値

        Returns:
            [type]: [description]
        """
        if _config == None or len(_config.COMMENT_OUT_LIST) == 0:
            return False

        # コメントアウトの行もgrep対象とする
        if _config.config["COMMENT_FLG"] == 'false':
            return True

        for commentOut in _config.COMMENT_OUT_LIST:
            # コメントアウトの文字を含んでいない
            if (commentOut in _line) is False:
                continue

            trimLine = Utility.trim(_line)

            # 先頭にコメントアウトの文字が記載されている場合
            if (trimLine.index(commentOut) <= 1):
                return True
        return False

    @staticmethod
    def trim(_str: str = ''):
        """[summary] TRIMを実行

        Args:
            _str (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        _str = _str.strip(' ')
        return _str
