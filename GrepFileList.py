import os
import glob
from Config import Config
from Utility import Utility


class GrepFileList:
    config: Config = None

    grepFileList = []

    def __init__(self, _config):
        """[summary]
        """
        print('開始 GrepFileList\r\n')
        self.config = _config
        self.grepFileList = []

    def fetchGrepFileList(self, path: str = ''):
        """[summary]
        grepの対象ファイルリストを取得する

        Args:
            path ([type]): [description] grep対象のフォルダーパス
        """
        pathList = self.__getDirOrFileList(path)
        for path in pathList:

            # パスがディレクトリの場合
            if (os.path.isdir(path)):
                # 再帰的に呼び出す
                self.fetchGrepFileList(path)

            # パスがファイルの場合
            elif(os.path.isfile(path)):
                self.grepFileList.append(path)

    def __getDirOrFileList(self, path: str = ''):
        """[summary] 配下のディレクトリまたはファイルリストを取得

        Args:
            path (str, optional): [description]. Defaults to ''.
        """
        returnPathList = []
        # 全ディレクトリ、ファイルを取得
        pathFullList = glob.glob(path + '\\*')

        for path in pathFullList:
            # grep対象のディレクトリかチェック
            if self.__isGrepTargetDir(path=path):
                returnPathList.append(path)
                continue

            # grep対象のファイルかチェック
            elif self.__isGrepTargetFile(path):
                returnPathList.append(path)
                continue

        return returnPathList

    def __isGrepTargetDir(self, path: str = ''):
        """[summary] grep対象のディレクトリかチェック

        Args:
            path ([type]): [description]

        Returns:
            [type]: [description]
        """
        # ディレクトリチェック
        if Utility.isDir(path=path) is False:
            return False

        baseName = os.path.basename(path)

        # 対象外のディレクトリかチェック
        for notTarget in self.config.config["NOT_TARGET_DIR_LIST"]:
            if baseName == notTarget:
                return False
        return True

    def __isGrepTargetFile(self, path):
        """[summary] grep対象のファイルかチェック

        Args:
            path ([type]): [description]

        Returns:
            [type]: [description]
            Ture 対象ファイル
            Flase 対象外ファイル
        """
        # ファイルチェック
        if Utility.isFile(path=path) is False:
            return False

        # ファイルの拡張子を取得
        root, ext = os.path.splitext(path)

        # 対象のファイルチェック
        for ng in self.config.NOT_TARGET_EXTENSION_LIST:
            # 読込対象外のファイル拡張子
            if ext == ng:
                return False

        # 対象のファイルチェック
        for ok in self.config.TARGET_EXTENSION_LIST:
            # *は全て
            if ok == '*':
                return True

            if ext == ok:
                return True
        return False
