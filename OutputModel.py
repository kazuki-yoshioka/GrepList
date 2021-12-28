from Config import Config


class OutputModel():
    targetChar = ''
    """[summary]grep対象の文字
    """

    fileName = ''
    """[summary] ファイル名
    """

    filePath = ''
    """[summary] ファイルパス
    """

    lineNo = ''
    """[summary]　行数
    """

    sheet = ''
    """[summary] シート名
    """

    cell = ''
    """[summary] セルの場所
    """

    line = ''
    """[summary] 行の文字列、または、セルの文字列
    """

    def __init__(self):
        self.__clear()

    def __clear(self):
        self.targetChar = ''
        self.fileName = ''
        self.filePath = ''
        self.lineNo = ''
        self.sheet = ''
        self.cell = ''
        self.line = ''

    @staticmethod
    def getCsvHeader():
        """[summary] CSVに出力する際のヘッダ部分を返却

        Returns:
            [type]: [description]
        """
        header = ''
        header = header + '対象文字'
        header = header + ','
        header = header + 'ファイル名'
        header = header + ','
        header = header + 'ファイルパス'
        header = header + ','
        header = header + '行数'
        header = header + ','
        header = header + 'シート'
        header = header + ','
        header = header + 'セル'
        header = header + ','
        header = header + '行の文字'
        header = header + '\n'

        return header

    def getCsvDetail(self):
        """[summary] CSVに出力する際の明細部分を返却

        Returns:
            [type]: [description]
        """
        detail = ''

        # grep対象の文字
        detail = detail + self.targetChar
        detail = detail + ','

        # ファイル名
        detail = detail + self.fileName
        detail = detail + ','

        # ファイルパス
        detail = detail + self.filePath
        detail = detail + ','

        # 行数
        detail = detail + self.lineNo
        detail = detail + ','

        # シート名
        detail = detail + self.sheet
        detail = detail + ','

        # セル
        detail = detail + self.cell
        detail = detail + ','

        # 行の文字
        detail = detail + self.line
        detail = detail + '\n'

        return detail

    def getJsonStr(self):
        """[summary] Json形式の文字列を返却する
        """
        jsonStr = '{'

        jsonStr = jsonStr + \
            self.Utility.makeJsonFormat('対象文字', self.targetChar)
        jsonStr = jsonStr + self.Utility.makeJsonFormat('ファイル名', self.fileName)
        jsonStr = jsonStr + \
            self.Utility.makeJsonFormat('ファイルパス', self.filePath)
        jsonStr = jsonStr + self.Utility.makeJsonFormat('行数', self.lineNo)
        jsonStr = jsonStr + self.Utility.makeJsonFormat('シート名', self.sheet)
        jsonStr = jsonStr + self.Utility.makeJsonFormat('セル', self.cell)
        jsonStr = jsonStr + self.Utility.makeJsonFormat('行の文字', self.line)

        jsonStr = jsonStr + '},'
        return jsonStr
