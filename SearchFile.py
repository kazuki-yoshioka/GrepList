import os
from Config import Config
from Utility import Utility
from WriteFile import WriteFile
from OutputModel import OutputModel


class SearchFile():
    resultList = []
    COMMENT_LIST = ['//', '#', '/*', '*', '<!--']
    config: Config = None

    def __init__(self, _config: Config):
        self.resultList = []
        self.config = _config
        self.config.setCommentOutList()

    def searchCharInFile(self, targetChar: str = '', path: str = ''):
        """[summary] ファイルから対象の文字を検索

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
        """
        try:
            lineNo = 1

            # ファイルの文字列を取得
            fileText = self.__getFileText(path=path)
            if fileText is None:
                return

            # １行ずつ読込
            for line in fileText:

                # 対象の文字を含む行の場合
                if self.__isTargetLine(line=line, targetChar=targetChar):
                    # ファイルのパス情報を追加
                    self.resultList.append(self.__makeFileInfo(
                        line=line, path=path, lineNo=lineNo, targetChar=targetChar))

                lineNo = lineNo + 1

        except Exception as e:
            print(e)

    def __getFileText(self,  path: str = ''):
        """[summary] ファイルの文字列を取得

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
            encoding (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        try:
            # shift-jisで文字を取得
            fileText = self.__getFileTextByEncoding(
                path=path, encoding='cp932')
            if fileText is not None:
                return fileText

            # utf-8で文字を取得
            self.__getFileTextByEncoding(path=path, encoding='utf-8')
            if fileText is not None:
                return fileText

            if self.config.config["READ_FILE_ENCODEING_CHACK"] == 'true':
                with open(path, 'r', encoding=Utility.getFileEncoding(path)) as f:
                    fileText = f.readlines()

            return fileText

        # 文字コードが異なる場合
        except Exception as e:
            print(e)

    def __getFileTextByEncoding(self,  path: str = '', encoding=''):
        """[summary] ファイルの文字列を取得

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
            encoding (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        try:
            if encoding == '':
                return None

            lineNo = 1
            with open(path, 'r', encoding=encoding) as f:
                fileText = f.readlines()

        # 文字コードが異なる場合
        except Exception as e:
            print(e)
            print('file: ' + path)
            fileText = None

        return fileText

    def __isTargetLine(self, line='', targetChar=''):
        """[summary] 対象行かチェック

        Args:
            line (str, optional): [description]. Defaults to ''.
            targetChar (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if line == '' or targetChar == '':
            return False

        # 対象の文字列を含んでいない
        if (targetChar in line) is False:
            return False

        # コメント行は抽出しない場合
        if Utility.isCommentLine(_line=line, _config=self.config):
            return False

        return True

    def __makeFileInfo(self, line: str = '', path: str = '', lineNo: int = 0, targetChar=''):
        """[summary] ファイル情報を作製

        Args:
            line (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
            lineNo (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        model = OutputModel()

        # grep対象文字
        model.targetChar = targetChar

        # ファイル名
        model.fileName = os.path.basename(path)

        # ファイルパス
        model.filePath = path

        # 行数
        model.lineNo = str(lineNo)

        # 行の文字列
        model.line = Utility.replaceNewLineCode(line)

        return model
