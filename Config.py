from posixpath import split
import json
from Utility import Utility


class Config():
    __CONFIG_FILE_PATH: str = 'config\\config.json'

    config = {}
    """ 設定値の辞書
    """

    NOT_TARGET_DIR_LIST = []
    """[summary] grep対象外のディレクトリリスト

    Returns:
        [type]: [description]
    """

    TARGET_EXTENSION_LIST = []
    """[summary] 読込対象の拡張子リスト

    Returns:
        [type]: [description]
    """

    NOT_TARGET_EXTENSION_LIST = []
    """[summary] 読込対象外の拡張子リスト

    Returns:
        [type]: [description]
    """

    EXCEL_EXTENSION_LIST = []
    """[summary] Excelの拡張子リスト

    Returns:
        [type]: [description]
    """

    COMMENT_OUT_LIST = []
    """[summary] コメントアウトの文字列リスト
    """

    def __init__(self):
        """[summary] 初期処理
        """
        self.clear()

        # コンフィグファイルを読込
        self._Config__readConfigFile()

        # 読込対象の拡張子リスト、読込対象外の拡張子リストを作製
        self.__makeTargetExtensionList()

        # Excelの拡張子リストを設定
        self.__setExcelExtensionList()
        return

    def clear(self):
        """[summary] クリア（初期化）
        """
        self.config = {}
        self.NOT_TARGET_DIR_LIST = []
        self.TARGET_EXTENSION_LIST = []
        self.EXCEL_EXTENSION_LIST = []
        self.COMMENT_OUT_LIST = []

    def __readConfigFile(self):
        """[summary] configファイルを読込 configの値を設定
        """
        with open(self._Config__CONFIG_FILE_PATH, 'r', encoding='shift_jis') as f:
            self.config = json.load(f)

        # キー: コメントを削除
        self.config.pop('COMMENT')

    def __makeTargetExtensionList(self):
        """[summary] 読込対象拡張子リストを作製

        Args:
            line (str, optional): [description]. Defaults to ''.
        """
        self.TARGET_EXTENSION_LIST = []
        self.NOT_TARGET_EXTENSION_LIST = []

        # デフォルトの読込対象外の拡張子をセット
        self.NOT_TARGET_EXTENSION_LIST.extend(
            self.config['DEFAULT_NOT_TARGET_EXTENSION'])

        # 読込対象拡張子リストでループ
        for ext in self.config['TARGET_EXTENSION_LIST']:

            # !が付いたものは読込対象外
            if '!' in str(ext):
                self.NOT_TARGET_EXTENSION_LIST.append(
                    str(ext).replace('!', ''))
            else:
                self.TARGET_EXTENSION_LIST.append(str(ext))

    def __setExcelExtensionList(self):
        self.EXCEL_EXTENSION_LIST = self.config['EXCEL_EXTENSION_LIST']

    def setCommentOutList(self, _ext=''):
        """[summary] コメントアウトリストを設定

        Args:
            _ext (str, optional): [description]. Defaults to ''.
        """
        self.COMMENT_OUT_LIST = []

        # コメントアウトの情報を取得
        for key, value in self.config['COMMENT_OUT'].items():
            if key == 'COMMENT':
                continue

            extList = value['EXTENSION']
            commentList = value['COMMENT']

            for ext in extList:
                # 対象の拡張子
                if (ext == _ext):
                    self.COMMENT_OUT_LIST = commentList
                    return
