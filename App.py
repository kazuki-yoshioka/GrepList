from Config import Config
from GrepFileList import GrepFileList
from SearchFile import SearchFile
from SearchExcelFile import SearchExcelFile
from WriteFile import WriteFile
from Utility import Utility


class App():

    TARGET_FILE_PATH = 'config\\TargetList.txt'
    targetCharList = []
    grepList = {}
    config = {}

    GREP_FILE_NO_NOT_TARGET = -1
    """[summary] grep対象が対象外
    """

    GREP_FILE_NO_TEXT = 1
    """[summary] grep対象がテキストファイル
    """

    GREP_FILE_NO_EXCEL = 2
    """[summary] grep対象がExcelファイル
    """

    def __init__(self):
        """[summary] 初期処理
        """
        self.config = Config()

        # grep対象の文字リストを作製
        self.__makeTargetCharList()

        # grep対象のファイルリストを作製
        self.grepList = GrepFileList(self.config)
        self.grepList.fetchGrepFileList(self.config.config["TARGET_DIR"])

    def execute(self):
        """[summary] 実行
        """
        print('実行\r\n')

        for char in self.targetCharList:
            # grep開始
            self.grep(targetChar=char)

    def grep(self, targetChar=''):
        """[summary] grep処理

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
        """
        print('getp開始 ' + targetChar + '\r\n')
        itemList = []
        for path in self.grepList.grepFileList:
            # 実行する処理を取得
            grepFileNo = self.__handleGrepFileNo(path=path)

            # テキストファイルの場合
            if grepFileNo == self.GREP_FILE_NO_TEXT:
                itemList.extend(self.__grepInTextfile(
                    targetChar=targetChar, path=path))

            # Excelファイルの場合
            elif grepFileNo == self.GREP_FILE_NO_EXCEL:
                itemList.extend(self.__grepInExcelfile(
                    targetChar=targetChar, path=path))

        # grep結果をファイルに書き込み
        self.__writeFile(targetChar=targetChar, itemList=itemList)

    def __handleGrepFileNo(self, path=''):
        """[summary] どのgrep処理を実行するのか操作（返却）する

        Args:
            path (str, optional): [description]. Defaults to ''.

        Returns:
            [type]: [description]
        """
        if path == '':
            return self.GREP_FILE_NO_NOT_TARGET

        # 拡張子を取得
        ext = Utility.getExtention(path=path)

        # Excelファイルの場合
        if Utility.isExcelExtention(ext=ext, excelExtensionList=self.config.config['EXCEL_EXTENSION_LIST']):
            return self.GREP_FILE_NO_EXCEL

        # 該当なしの場合、テキストファイルを返却
        return self.GREP_FILE_NO_TEXT

    def __grepInTextfile(self, targetChar='', path=''):
        """[summary] テキストファイル内でgrepを実施する

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
        """
        searchFile = SearchFile(self.config)

        # １ファイルを検索
        searchFile.searchCharInFile(targetChar=targetChar, path=path)

        # grep結果を返却
        return(searchFile.resultList)

    def __grepInExcelfile(self, targetChar='', path=''):
        """[summary] テキストファイル内でgrepを実施する

        Args:
            targetChar (str, optional): [description]. Defaults to ''.
            path (str, optional): [description]. Defaults to ''.
        """
        searchFile = SearchExcelFile(self.config)

        # １ファイルを検索
        searchFile.searchCharInFile(targetChar=targetChar, path=path)

        # grep結果を返却
        return(searchFile.resultList)

    def __writeFile(self, targetChar, itemList):
        """[summary] ファイルに書き込む

        Args:
            targetChar ([type]): [description]
            itemList ([type]): [description]
        """
        wf = WriteFile(targetChar=targetChar)
        wf.writeFile(_list=itemList)

    def __makeTargetCharList(self):
        """[summary] grep対象の文字列を取得
        """
        self.targetCharList = []
        with open(self.TARGET_FILE_PATH, 'r', encoding='shift_jis') as f:
            fileText = f.readlines()

            for line in fileText:
                v = Utility.replaceNewLineCode(line=line)
                self.targetCharList.append(v)


app = App()
app.execute()
