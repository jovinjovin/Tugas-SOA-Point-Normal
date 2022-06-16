import dependencies

from nameko.rpc import rpc

class FileService:

    name = 'file_service'

    database = dependencies.Database()

    @rpc
    def upload_file(self, file):
        news = self.database.upload_file(file)
        return news

    @rpc
    def download_file(self, id):
        news = self.database.download_file(id)
        return news